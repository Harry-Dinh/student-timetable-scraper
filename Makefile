# Fetch course work grades
getGrades:
	python3 gradescraper.py

# Fetch the student timetable
getTimetable:
	python3 timetablescraper.py

# Fetch the final grades
getFinals:
	python3 finalgradescraper.py

# Remove all of the HTML files
clean:
	rm -f *.html