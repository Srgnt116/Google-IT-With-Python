#!/usr/bin/env python3

import json
import locale
import sys
import reports
import emails
import os
import os.path

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = 0
  pop_year = {}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    if item["total_sales"] > max_sales:
      max_sales_car = item
      max_sales = item["total_sales"]
    # TODO: also handle most popular car_year
    year = format_car(item["car"])[len(format_car(item["car"]))-5:
      len(format_car(item["car"]))-1]
    if year not in pop_year.keys():
      pop_year[year] = item["total_sales"]
    else:
      pop_year[year] += item["total_sales"]
  sorted_pop_year = sorted(pop_year.items(), key=lambda item: item[1], reverse=True)
  high_pop_year, cumulative_sales = sorted_pop_year[0]
  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(
      format_car(max_sales_car["car"]), max_sales),
    "The most popular year was {} with {} sales".format(
      high_pop_year, cumulative_sales)
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  print(summary)
  # TODO: turn this into a PDF report
  max_rev_car, max_sales_car, max_year = summary
  table_data = cars_dict_to_table(data)
  reports.generate(
    "/tmp/cars.pdf",
    "Sales summary for last month",
    "{}<br/>{}<br/>{}".format(max_rev_car, max_sales_car, max_year),
    table_data
  )
  # TODO: send the PDF report as an email attachment
  sender = "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body = "{}\n{}\n{}".format(max_rev_car, max_sales_car, max_year)

  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)

if __name__ == "__main__":
  main(sys.argv)