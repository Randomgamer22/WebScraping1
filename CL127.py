from bs4 import BeautifulSoup
import requests
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

r = requests.get(START_URL)

def scrape():
	headers = ["Name", "Distance", "Mass", "Radius"]
	star_data = []

	soup = BeautifulSoup(r.text, "html.parser")
	table = soup.find("tbody")

	for tr_tag in table.find_all("tr"):
		td_tags = tr_tag.find_all("td")
	
		temp_list = []

		for index, td_tag in enumerate(td_tags):
			if index == 1:
				temp_list.append(r'{}'.format(td_tag.contents[0]))

			elif index == 3 or index == 5 or index == 6:
				try:
					temp_list.append(r'{}'.format(td_tag.contents[-1]))

				except:
					temp_list.append("")

		star_data.append(temp_list)

	return star_data, headers	

def find_letter(str, ch):
	index_list = []

	for i, ltr in enumerate(str):
		if ltr == ch:
			index_list.append(i)

	return index_list
			

def basic_filter(data):
	new_data = []

	for star_data in data:
		unfiltered_string = str(star_data[0])
		unfiltered_distance = str(star_data[1])
		unfiltered_mass = str(star_data[2])
		unfiltered_radius = str(star_data[3])

		if '</a>' in unfiltered_string:
			start = find_letter(unfiltered_string, ">")[0]
			end = find_letter(unfiltered_string, "<")[-1]
			# print(r'{}, {}'.format(start, end))
			# print("found")
			star_data[0] = unfiltered_string[start+1:end]

		if '\n' in unfiltered_string:
			star_data[0] = unfiltered_string.replace('\n', '')

		if '\n' in unfiltered_distance:
			star_data[1] = unfiltered_distance.replace('\n', '')

		if '\n' in unfiltered_mass:
			star_data[2] = unfiltered_mass.replace('\n', '')

		if '\n' in unfiltered_radius:
			star_data[3] = unfiltered_radius.replace('\n', '')


		# print('{}, {}, {}, {}'.format(star_data[0], star_data[1], star_data[2], star_data[3]))

		new_data.append(star_data)

	return new_data


star_data, headers = scrape()
del star_data[0]

star_data = basic_filter(star_data)

# print(star_data)

with open("./result/main.csv", "w") as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow(headers)
	csv_writer.writerows(star_data)

