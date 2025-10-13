import hashlib
import json
from time import time

class Block:
    def __init__(self, idx, student_data, previous_hash, timestamp=None, nonce=0, difficulty=4, hash_val=None):
        self.idx = idx
        self.student_data = student_data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.timestamp = timestamp if timestamp else time()
        
        #preserve stored hash when loading, verify integrity
        if hash_val is not None:
            #when loading existing block, use stored hash but verify
            self.hash = hash_val
            calculated_hash = self.compute_hash()
            if calculated_hash != self.hash:
                print(f"⚠️  Block {idx}: Data was modified outside blockchain!")
        else:
            #when creating new block, compute hash
            self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.idx,
            "timestamp": self.timestamp,
            "student_data": self.student_data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self):
        prefix = "0" * self.difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self, filename="blockchain.json"):
        self.chain = []
        self.filename = filename
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, {"message": "Genesis Block"}, "0")
        genesis_block.mine_block()
        self.chain.append(genesis_block)
        self.save_chain()

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    def add_block(self, student_data, difficulty=4):
        if not self.chain:
            self.create_genesis_block()
            
        index = len(self.chain)
        previous_hash = self.last_block.hash
        new_block = Block(index, student_data, previous_hash, difficulty=difficulty)
        new_block.mine_block()
        self.chain.append(new_block)
        self.save_chain()
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                print(f"Block {current.idx}: Hash mismatch!")
                return False
            if current.previous_hash != previous.hash:
                print(f"Block {current.idx}: Chain link broken!")
                return False
        return True

    def display_chain(self):
        for block in self.chain:
            print(f"Index: {block.idx}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.student_data}")
            print(f"Nonce: {block.nonce}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}\n")

    def save_chain(self):
        chain_data = []
        for block in self.chain:
            chain_data.append({
                "idx": block.idx,
                "timestamp": block.timestamp,
                "student_data": block.student_data,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash
            })
        with open(self.filename, "w") as f:
            json.dump(chain_data, f, indent=4)

    def load_chain(self):
        try:
            with open(self.filename, "r") as f:
                chain_data = json.load(f)
                for b in chain_data:
                    block = Block(
                        idx=b["idx"],
                        student_data=b["student_data"],
                        previous_hash=b["previous_hash"],
                        timestamp=b["timestamp"],
                        nonce=b.get("nonce", 0),
                        hash_val=b["hash"]  #pass stored hash
                    )
                    self.chain.append(block)
        except (FileNotFoundError, json.JSONDecodeError):
            self.create_genesis_block()

    def fix_blockchain_integrity(self):
        #fix any hash inconsistencies in the blockchain
        print("🔧 Fixing blockchain integrity...")
        for i in range(len(self.chain)):
            block = self.chain[i]
            calculated_hash = block.compute_hash()
            if block.hash != calculated_hash:
                print(f"🛠️  Fixing Block {block.idx} hash")
                block.hash = calculated_hash
        

        for block in self.chain:
            if not block.hash.startswith("0" * block.difficulty):
                block.mine_block()
        
        self.save_chain()
        print("Blockchain integrity fixed!")