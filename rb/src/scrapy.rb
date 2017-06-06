require 'httparty'
require 'nokogiri'
require 'json'
require 'pry'


target_url = 'http://www.jonkolko.com/projectFiles/scad/'

page = HTTParty.get(target_url)
parse_page = Nokogirl::HTML(page)

Pry.start(binding)

puts Pry(main)>parse_page
