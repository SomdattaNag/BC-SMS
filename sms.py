import re
import copy
from blockchain import Blockchain

chain = Blockchain()

class SMS:
    Subjects = {
        '1': ['Physics','Mathematics-I','Introduction to Electrical Engineering'],
        '2': ['Programming in C', 'Mathematics-II', 'English', 'Chemistry'],
        '3': ['ADE','DSA','Computer Organization','Economics for Engineers','Mathematics-III'],
        '4': ['DAA','Computer Architecture','Discrete Math','Theory of Automata','Biology','EVS'],
        '5': ['Operating Systems','OOPs in Java','Software Engineering','Compiler Design','Artificial Intelligance'],
        '6': ['DBMS','Computer Networks','Data Mining','Distributed Systems','Numerical Methods'],
        '7': ['Cyber Security','Machine Learning','Cloud Computing', 'Project Management'],
        '8': ['Cryptography and Network Security', 'Speech and Natural Language Processing', 'Web and Internet Technology', 'Internet of Things']
    }

    def __init__(self):
        self.name=None
        self.roll=None
        self.email=None
        self.sem=None
        self.contact=None
        self.marks={}

    #variable validation methods
    def validate_name(self, name):
        return bool(re.match(r"^[A-Za-z ]+$", name))

    def validate_roll(self, roll):
        return bool(re.match(r"^[A-Za-z0-9]+$", roll))

    def validate_email(self, email):
        return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", email))

    def validate_contact(self, contact):
        return contact.isdigit() and len(contact) == 10

    def validate_semester(self, sem):
        return sem in SMS.Subjects

    #initializing student data as dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "roll": self.roll,
            "email": self.email,
            "semester": self.sem,
            "contact": self.contact,
            "marks": self.marks
        }

    #fetch latest student data from blockchain
    def get_latest_student_data(self, include_deleted=False):
        for block in reversed(chain.chain):
            data=block.student_data
            if isinstance(data, dict) and data.get("roll") == self.roll:
                if data.get("deleted") and not include_deleted:
                    return None
                return data
        return None

    #Main Methods Start
    
    def get_full_history(self):
        history= []
        for block in chain.chain:
            data = block.student_data
            if isinstance(data, dict) and data.get("roll") == self.roll:
                history.append({
                    "block_number": block.idx,  
                    "timestamp": block.timestamp,
                    "data": data
                })
        return history

    def add_student_details(self):
        #reset all instance variables before adding new student
        self.name=None
        self.roll=None
        self.email=None
        self.sem=None
        self.contact=None
        self.marks={}

    #name validation
        while True:
            self.name=input('Enter Name of Student: ').strip()
            if not self.name:
                print("⚠ Name cannot be empty!")
                continue
            if self.validate_name(self.name):
                break
            print("⚠ Invalid name! Use only alphabets and spaces.")

        while True:
            roll = input('Enter Roll No.: ').strip()
            if not roll:
                print("⚠ Roll number cannot be empty!")
                continue
            if not self.validate_roll(roll):
                print("⚠ Invalid roll number! Use only letters and numbers.")
                continue

        
            temp=self.roll  
            self.roll=roll  
        
            existing_student=self.get_latest_student_data()
        
            if existing_student and not existing_student.get("deleted"):
                print("⚠ Student with this roll number already exists!")
                self.roll=temp 
                continue
            self.roll = temp 
            break
        self.roll= roll

        while True:
            self.email = input('Enter Email Id: ').strip()
            if not self.email:
                print("⚠ Email cannot be empty!")
                continue
            if self.validate_email(self.email):
                break
            print("⚠ Invalid email format! Example: abc@gmail.com")

        while True:
            self.sem =input('Enter Semester (1-8): ').strip()
            if not self.sem:
                print("⚠ Semester cannot be empty!")
                continue
            if self.validate_semester(self.sem):
                break
            print("⚠ Invalid semester! Please enter a number between 1 and 8.")

        while True:
            self.contact =input('Enter Contact No.: ').strip()
            if not self.contact:
                print("⚠ Contact number cannot be empty!")
                continue
            if self.validate_contact(self.contact):
                break
            print("⚠ Invalid contact number! Must be 10 digits only.")

        print("\n" + "-"*40)
        print("PLEASE CONFIRM STUDENT DETAILS:")
        print(f"Name     : {self.name}")
        print(f"Roll No  : {self.roll}")
        print(f"Email    : {self.email}")
        print(f"Semester : {self.sem}")
        print(f"Contact  : {self.contact}")
        print("-"*40)
    
        confirm =input("\n Do you onfirm adding this student? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Student addition cancelled.")
            return

        chain.add_block(self.to_dict())
        print("Student details added successfully!")

    def update_student_details(self):
        current_roll =input("Enter Roll No. of the student to update: ")
        self.roll =current_roll
        
        latest =self.get_latest_student_data()
        if not latest:
            print("No student record found on blockchain. Add first.")
            return
        if latest.get("deleted"):
            print("Cannot update. Student has been deleted.")
            return

        updated_data =latest.copy()

        while True:
            print('\nWhat would you like to update?') 
            print('1. Name')
            print('2. Roll No.') 
            print('3. Email Id')
            print('4. Semester')
            print('5. Contact No.')
            print('6. Save Changes and Exit')
            print('7. Cancel without saving')
            
            ch = input('Enter your choice: ')
            
            if ch =='1':
                while True:
                    name = input('Enter Name of Student: ')
                    if self.validate_name(name):
                        updated_data['name'] = name
                        print("✓ Name updated successfully!")
                        break
                    print("⚠ Invalid name! Use only alphabets and spaces.")
                    
            elif ch=='2':
                while True:
                    new_roll = input('Enter new Roll No.: ')
                    if not self.validate_roll(new_roll):
                        print("⚠ Invalid roll number! Use only letters and numbers.")
                        continue
                    
                    if new_roll != current_roll:
                        temp_roll = self.roll
                        self.roll = new_roll
                        existing = self.get_latest_student_data()
                        self.roll = temp_roll
                        
                        if existing and not existing.get("deleted"):
                            print("⚠ Another student with this roll number already exists!")
                            continue
                    
                    updated_data['roll'] = new_roll
                    print("✓ Roll number updated successfully!")
                    break
                    
            elif ch=='3':
                while True:
                    email = input('Enter new Email Id: ')
                    if self.validate_email(email):
                        updated_data['email'] = email
                        print("✓ Email updated successfully!")
                        break
                    print("⚠ Invalid email format! Example: abc@gmail.com")
                    
            elif ch=='4':
                while True:
                    sem = input('Enter new Semester (1-8): ')
                    if self.validate_semester(sem):
                        updated_data['semester'] = sem
                        print("✓ Semester updated successfully!")
                        break
                    print("⚠ Invalid semester! Please enter a number between 1 and 8.")
                    
            elif ch=='5':
                while True:
                    contact = input('Enter new Contact No.: ')
                    if self.validate_contact(contact):
                        updated_data['contact'] = contact
                        print("✓ Contact number updated successfully!")
                        break
                    print("⚠ Invalid contact number! Must be 10 digits only.")
                    
            elif ch=='6':
                chain.add_block(updated_data)
                print("✓ Student record updated successfully!")
                break
            
            elif ch=='7':
                print("Update cancelled. No changes saved.")
                break
            
            else:
                print('Invalid choice. Please select 1-7.')

    def upload_marks(self):
        latest = self.get_latest_student_data()
        if not latest:
            print("⚠ No student record found on blockchain. Add first.")
            return
        if latest.get("deleted"):
            print("⚠ Cannot upload marks. Student has been deleted.")
            return
        self.name=latest['name']
        self.roll = latest['roll']
        self.email = latest['email']
        self.sem = latest['semester']  
        self.contact = latest['contact']
        self.marks = latest.get('marks', {}).copy()

        while True:
            sem = input("Enter semester to upload marks (1-8): ")
            if self.validate_semester(sem):
                break
            print("⚠ Invalid semester! Please enter a number between 1 and 8.")

    
        if sem != self.sem:
            print(f"⚠ Cannot upload marks for semester {sem}. Student is currently in semester {self.sem}.")
            print("   You can only upload marks for your current semester.")
            return

        if sem in self.marks and self.marks[sem]:
            print(f"⚠ Marks for semester {sem} are already uploaded!")
            print("   Existing marks:", self.marks[sem])
            choice = input("   Do you want to update instead? (y/n): ").strip().lower()
            if choice.lower() == 'y':
                self.update_marks()  
                return
            else:
                print("Upload cancelled.")
                return

        if sem not in self.marks:
            self.marks[sem] = {}

        print(f"Uploading marks for semester {sem}...")
        for subject in SMS.Subjects[sem]:
            while True:
                try:
                    mark = int(input(f"Enter marks for {subject}: "))
                    if 0 <= mark <= 100:
                        self.marks[sem][subject] = mark
                        break
                    else:
                        print("Marks should be between 0 and 100.")
                except ValueError:
                    print("Please enter a valid integer.")

        chain.add_block(self.to_dict())
        print("\nMarks Uploaded Successfully!")

    def display_student(self):
        latest = self.get_latest_student_data()
        if not latest:
            print("⚠ No student record found on blockchain.")
            return
        if latest.get("deleted"):
            print("⚠ This student has been deleted.")
            return

        print("\n--------------- STUDENT DETAILS ---------------")
        print(f"Name      : {latest['name']}")
        print(f"Roll No   : {latest['roll']}")
        print(f"Email ID  : {latest['email']}")
        print(f"Contact No: {latest['contact']}")
        print(f"Semester  : {latest['semester']}")
        print("----------------------------------------------")

    def update_marks(self):
        roll= self.roll
        if not roll:
            print("⚠ No roll number specified!")
            return

        latest = self.get_latest_student_data()
        if not latest:
            print("⚠ No student record found on blockchain. Add first.")
            return
        if latest.get("deleted"):
            print("⚠ Cannot update marks. Student has been deleted.")
            return

        updated_data = {
            "name": latest['name'],
            "roll": latest['roll'], 
            "email": latest['email'],
            "semester": latest['semester'],
            "contact": latest['contact'],
            "marks": copy.deepcopy(latest.get('marks', {})) #creating a deep copy to avoid mutating original data
        }

        print(f"\nUpdating marks for: {updated_data['name']} (Roll: {updated_data['roll']})")
        print(f"Current Semester: {updated_data['semester']}")

        available_semesters = [sem for sem in updated_data['marks'] if updated_data['marks'][sem] and sem in SMS.Subjects]
    
        if not available_semesters:
            print("⚠ No marks uploaded for any semester yet.")
            
            #Offer to upload marks for current semester
            if updated_data['semester'] in SMS.Subjects:
                choice = input(f"Would you like to upload marks for current semester {updated_data['semester']}? (y/n): ").strip().lower()
                if choice == 'y':
                #for uploading marks, setting instance variables
                    self.name = updated_data['name']
                    self.roll = updated_data['roll']
                    self.email = updated_data['email']
                    self.sem = updated_data['semester']
                    self.contact = updated_data['contact']
                    self.marks = updated_data['marks']
                    self.upload_marks()
            return

        print(f"Available semesters with marks: {', '.join(available_semesters)}")
    
        while True:
            sem= input("Enter semester to update marks: ").strip()
            if not sem:
                print("Enter Semester")
                continue
            if sem in available_semesters:
                break
            print(f"No marks found for semester {sem}. Available: {', '.join(available_semesters)}")

        print(f"\nUpdating marks for semester {sem}:")
        print("-" * 50)
    
        marks_updated=False
        for subject in SMS.Subjects[sem]:
            curr_mark=updated_data['marks'][sem].get(subject, "Not entered")
            prompt=f"Enter marks for {subject} (current: {curr_mark}): "
    
            while True:
                try:
                    mark_input = input(prompt).strip()
                    if mark_input=="":  #skipping if empty
                        print(f"  Keeping current marks for {subject}")
                        break
                
                    mark = int(mark_input)
                    if 0 <= mark <= 100:
                        if mark != updated_data['marks'][sem].get(subject):  #only update if changed
                            updated_data['marks'][sem][subject] = mark
                            marks_updated = True
                        break
                    else:
                        print("Marks should be between 0 and 100.")
                except ValueError:
                    print("Please enter a valid integer or press Enter to skip.")

        if not marks_updated:
            print("No marks were updated.")
            return

        print("\n" + "="*50)
        print("MARKS SUMMARY (Updated subjects):")
        print("="*50)
        for subject in SMS.Subjects[sem]:
            if subject in updated_data['marks'][sem]:
                print(f"{subject:<45} : {updated_data['marks'][sem][subject]}")
        print("="*50)

        confirm = input("Confirm updating these marks? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Marks update cancelled.")
            return

        chain.add_block(updated_data)
        print("✅ Marks updated successfully!")
    def display_marks(self):
        latest = self.get_latest_student_data()
        if not latest:
            print("⚠ No student record found on blockchain.")
            return
        if latest.get("deleted"):
            print("⚠ This student has been deleted.")
            return

        marks_data = latest.get('marks', {})
        
        while True:
            sem = input("Enter semester to view marks (1-8): ")
            if self.validate_semester(sem):
                break
            print("⚠ Invalid semester! Please enter a number between 1 and 8.")

        if sem not in marks_data or not marks_data[sem]:
            print(f"⚠ No marks uploaded yet for Semester {sem}.")
            return

        print("\n====================================  MARKSHEET  ====================================")
        print(f"Name      : {latest['name']}")
        print(f"Roll No   : {latest['roll']}")
        print(f"Semester  : {sem}")
        print("==============================================================================================")
        print(f"{'Subject':50}Marks")
        print("----------------------------------------------------------------------------------------------")

        total = 0
        count = 0
        for subject in SMS.Subjects[sem]:
            mark = marks_data[sem].get(subject, "N/A")
            print(f"{subject:50}{mark}")
            if isinstance(mark, int):
                total += mark
                count += 1

        if count > 0:
            percentage = total / count
            print("----------------------------------------------------------------------------------------------")
            print(f"Total Marks : {total}")
            print(f"Percentage  : {percentage:.2f}%")
        print("==============================================================================================")

    def delete_student(self):
        latest = self.get_latest_student_data()
        if not latest:
            print("⚠ No student record found on blockchain.")
            return

        confirm = input(f"Are you sure you want to delete {latest['name']}'s record? (y/n): ")
        if confirm.lower() == 'y':
            deleted_data = latest.copy()
            deleted_data["deleted"] = True
            chain.add_block(deleted_data)
            print("Student deleted Successfully!")
        else:
            print("Deletion cancelled.")

def admin(obj):
    print("\n================= Welcome to the Student Management System =================")
    while True:
        print("\n================= STUDENT MANAGEMENT SYSTEM =================")
        print("1. Add Student Details")
        print("2. Display Student Details")
        print("3. Upload Marks")
        print("4. Update Marks")
        print("5. Display Marksheet")
        print("6. Update Student Details")
        print("7. Delete Student Record")
        print("8. View Full Student History")
        print("9. Exit")
        print("=============================================================")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if choice==1:
            obj.add_student_details()
        elif choice==2:
            roll = input("Enter Roll No. of the student to display: ")
            obj.roll = roll
            obj.display_student()
        elif choice == 3:
            roll = input("Enter Roll No. of the student to upload marks: ")
            obj.roll = roll
            obj.upload_marks()
        elif choice==4:
            roll=input("Enter Roll No. of the student you want to update marks: ")
            obj.roll = roll
            obj.update_marks()
        elif choice == 5:
            roll = input("Enter Roll No. of the student to display marks: ")
            obj.roll = roll
            obj.display_marks()
        elif choice==6:
            obj.update_student_details()
        elif choice == 7:
            roll = input("Enter Roll No. of the student to delete: ")
            obj.roll=roll
            obj.delete_student()
        elif choice == 8:
            roll = input("Enter Roll No. of the student to view history: ")
            obj.roll = roll
            history = obj.get_full_history()
            if not history:
                print("⚠ No history found for this student.")
            for i, h in enumerate(history, 1):
                print(f"\n {i} : {h}")
        elif choice == 9:
            print("👋 Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def student(obj):
    print("\n================= Welcome to the Student Management System =================")
    while True:
        print("\n================= STUDENT MANAGEMENT SYSTEM =================")
        print("1. Display Student Details")
        print("2. Display Marksheet")
        print("3. Exit")
        print("=============================================================")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if choice == 1:
            roll = input("Enter your Roll No.: ")
            obj.roll = roll
            obj.display_student()
        elif choice == 2:
            roll = input("Enter your Roll No.: ")
            obj.roll = roll
            obj.display_marks()
        elif choice == 3:
            print("👋 Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

obj=SMS()
admin(obj)