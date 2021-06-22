## gpa.py

Example script that computes the mean of an array of GPAs and checks that they match an expected average GPA.

Input: Array of GPAs

Output: Average GPA

Cost: 841 constraints with commitment checks, 37 constraints without commitment checks

## covidCases.py

Computes the percentage of total COVID cases in Massachussets per age range and checks that they match a published result.

Input: The number of COVID cases in Massachussets broken down by age range

Output: The percentage of COVID cases per age range

Cost: 1220 constraints with commitment checks, 16 constraints without commitment checks

## degreesAwarded.py

Computes the percentage of students at Boston University that graduated broken down by year of matriculation and by degree length. Checks that they match the [statistics published on IPEDS](https://nces.ed.gov/ipeds/datacenter/InstitutionProfile.aspx?unitid=164988) (See Retention and Graduation).

Input: Database of students and their graduation status, broken down by degree length and start year

Output: The graduation percentage by degree length and start year

Cost: 53434 constraints with commitment checks, 3030 constraints without commitment checks

### Technical Details

Students that graduated are represented by a 1, while students that did not graduate are represented with a 0.

Students that started in 2013 have 10 added to their representation. Students starting in 2013 that graduated are represented as an 11, while those that did not are represented by a 10.

## distanceEducation.py

Computes the percentage of students at Boston University in distance education status before and after Boston University implemented the Learn from Anywhere modality. Checks that they match the [statistics published on IPEDS](https://nces.ed.gov/ipeds/datacenter/InstitutionProfile.aspx?unitid=164988) (See Enrollment).

Input: A database of students and their distance education status pre-LFA, and a database of students and their distance education status post-LFA

Output: The percentage of students in distance education by distance education type for pre-LFA and post-LFA students

Cost: 44226 constraints with commitment checks, 3822 constraints without commitment checks

### Technical Details

Students in full distance education are represented by a 1.

Students in some form of distance education other than full are represented by a 2.

Students not enrolled in distance education are represented by a 3.

## netPriceByIncome.py

Computes the average net tuition paid by students per income bracket at Boston University. Checks that they match the [statistics published on IPEDS](https://nces.ed.gov/ipeds/datacenter/InstitutionProfile.aspx?unitid=164988) (See Net Price).

Input: Database of students, their incomes, and their net tuition paid

Output: The average net tuition paid per income bracket

Cost: 150434 constraints with commitment checks, 30 constraints without commitment checks

## outcomeMeasures.py

Computes the graduation and transfer rates for students with and without Pell grants at Boston University broken down by matriculation year and study mode (Full time vs. Part time). Checks that they match the [statistics published on IPEDS](https://nces.ed.gov/ipeds/datacenter/InstitutionProfile.aspx?unitid=164988) (See Outcome Measures).

Input: Database of students and their graduation or transfer status, broken down by matriculation year and study mode

Output: The percentages of students that graduated, stayed, or transferred, broken down by matriculation year and study mode

Cost: 63336 constraints with commitment checks, 22932 constraints without commitment checks

### Technical Details

Students that received a Bachelor's degree at Boston University are represented by a 1.

Students that have not received a Bachelor's degree but are still enrolled at Boston University are represented by a 2.

Students that have not received a Bachelor's degree and have enrolled at an institution other than Boston University are represented by a 3.

Students receiving Pell grants have a 10 added to their representation. For example, students receiving Pell grants who received a Bachelor's degree at Boston University are represented by an 11.