def verify_blockchain_integrity(filename="blockchain.json"):
    """External function to verify blockchain integrity"""
    import hashlib
    import json
    
    print("\n" + "="*70)
    print("🔍 EXTERNAL BLOCKCHAIN INTEGRITY VERIFICATION")
    print("="*70)
    
    try:
        with open(filename, "r") as f:
            chain_data = json.load(f)
    except FileNotFoundError:
        print("❌ Blockchain file not found!")
        return False
    
    if not chain_data:
        print("❌ Empty blockchain!")
        return False
    genesis = chain_data[0]
    print(f"\n📦 GENESIS BLOCK VERIFICATION:")
    print(f"   Index: {genesis['idx']} (should be 0) - {'✅' if genesis['idx'] == 0 else '❌'}")
    print(f"   Previous Hash: '{genesis['previous_hash']}' (should be '0') - {'✅' if genesis['previous_hash'] == '0' else '❌'}")

    print(f"\n🔗 BLOCK-BY-BLOCK INTEGRITY CHECK:")
    all_blocks_valid = True
    
    for i in range(len(chain_data)):
        block = chain_data[i]
        block_string = json.dumps({
            "index": block["idx"],
            "timestamp": block["timestamp"],
            "student_data": block["student_data"],
            "previous_hash": block["previous_hash"],
            "nonce": block["nonce"]
        }, sort_keys=True).encode()
        
        calculated_hash = hashlib.sha256(block_string).hexdigest()
        hash_valid = (calculated_hash == block["hash"])
        pow_valid = block["hash"].startswith("0000")  
        link_valid = True
        if i > 0:
            link_valid = (block["previous_hash"] == chain_data[i-1]["hash"])
        
        block_valid = hash_valid and pow_valid and link_valid
        all_blocks_valid = all_blocks_valid and block_valid
        
        status = "✅ VALID" if block_valid else "❌ TAMPERED"
        print(f"   Block {block['idx']}: {status}")
        print(f"     Hash integrity: {'✅' if hash_valid else '❌'} (stored: {block['hash'][:20]}...)")
        print(f"     POW valid: {'✅' if pow_valid else '❌'}")
        if i > 0:
            print(f"     Chain link: {'✅' if link_valid else '❌'}")
    print(f"\n🔒 TAMPERING DETECTION TESTS:")
    print("\n" + "="*70)
    if all_blocks_valid:
        print("🎉 BLOCKCHAIN INTEGRITY: ✅ PERFECT - No tampering detected!")
        print(f"   Total blocks: {len(chain_data)}")
        print(f"   Latest block timestamp: {chain_data[-1]['timestamp']}")
    else:
        print("🚨 BLOCKCHAIN INTEGRITY: ❌ COMPROMISED - Tampering detected!")
    
    print("="*70)
    return all_blocks_valid


if __name__ == "__main__":
    verify_blockchain_integrity()