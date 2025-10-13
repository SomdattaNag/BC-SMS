# BC-SMS

A BLOCKCHAIN based student management system for storing & verifying student data securely.

## Overview

**BC-SMS** leverages blockchain technology to manage, store, and verify student data securely. By using decentralized data structures, the system enhances data integrity, transparency, and security for educational institutions and students.

## Blockchain Features

- Secure storage of student records using blockchain principles
- Easy verification of student data
- Tamper-proof history tracking
- Python-based implementation

## Admin View features

1. Add Student Details
    - Register new students in the system
    - Input: Name, Roll Number, Email, Semester, Contact
    - Automatic duplicate roll number validation
    - Data validation for all fields
    - Blockchain storage of student records

2. Display Student Details
    - View complete student information
    - Search by roll number
    - Display: Name, Roll, Email, Contact, Semester
    - Real-time data from blockchain

3. Upload Marks
    - Add marks for current semester subjects
    - Input marks for all subjects (0-100 range)
    - Semester validation (only current semester allowed)
    - Prevents duplicate mark uploads
    - Automatic percentage calculation

4. Update Marks
    - Modify existing marks for any semester
    - View current marks before updating
    - Selective subject mark updates
    - Change confirmation before saving
    - Maintains mark history in blockchain

5. Display Marksheet
    - Generate formatted marksheets
    - Show subject-wise marks
    - Calculate total marks and percentage
    - Semester-specific marks display
    - Professional marksheet formatting

6. Update Student Details
     - Modify student personal information
     - Update: Name, Roll, Email, Semester, Contact
     - Roll number uniqueness validation
     - Field-by-field updating option
     - Change confirmation system

7. Delete Student Record
    - Soft delete student records
    - Marks record as "deleted" in blockchain
    - Confirmation prompt before deletion
    - Preserves historical data
    - Prevents accidental deletions

8. View Full Student History
    - Complete audit trail of all changes
    - Shows all blockchain transactions for a student
    - Timestamp of each modification
    - Historical data preservation
    - Complete transparency

## Student View Features

1. Display Student Details
   - View own personal information
   - Access: Name, Roll, Email, Contact, Semester
   - Read-only access to personal data
   - Real-time data retrieval

2. Display Marksheet
   - View own marks and grades
   - Semester-wise marks display
   - Subject-wise performance
   - Total marks and percentage
   - Formatted marksheet output


## Usage

- To run the blockchain and student management system, execute:
  ```sh
  python sms.py
  ```
- For blockchain-specific functionality:
  ```sh
  python blockchain.py
  ```
- To perform data integrity checks:
  ```sh
  python check.py
  ```

## Project Structure

- `blockchain.py` &mdash; Core blockchain logic and data management
- `check.py` &mdash; Scripts to check and verify data
- `sms.py` &mdash; Main application logic for the student management system
- `blockchain.json` &mdash; Contains dummy data to show how the blockchain stores data.




