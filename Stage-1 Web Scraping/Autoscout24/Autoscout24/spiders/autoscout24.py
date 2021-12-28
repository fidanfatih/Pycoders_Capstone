import scrapy
#scrapy crawl autoscout24 -o autoscout_data.json
#scrapy crawl autoscout24 -o autoscout_data.csv

class Autoscout24Spider(scrapy.Spider):
    name = 'autoscout24'
    start_urls = ['https://www.autoscout24.com']

    countries = {
                 'NL':'Netherlands',
                 # 'D':'Germany',
                 # 'F':'France',
                 }
    makes =['audi',
            'bmw','ford',
            'mercedes-benz','opel','volkswagen',
            'renault','citroen','chevrolet','dacia',
            'fiat','honda','hyundai','kia','mazda',
            'peugeot','skoda','toyota','tesla','volvo',
            ]
    fuel_types= {'B':'Gasoline',
                 'D':'Diesel', 'E':'Electric', '2':'Electric/Gasoline', '3':'Electric/Diesel', 'C%2CH%2CL%2CM%2CO':'Other',
                 }
    body_types= {
        '1':'Compact','2':'Convertible','3':'Coupe','4':'Off-Road/Pick-up','5':'Station wagon',
        '6':'Sedans',
        '7':'Other','12':'Van','13':'Transporter',
    }
    gears={'A':'Automatic',
           'M':'Manuel','S':'Semi-automatic',
           }
    pages = range(1,21)
    # pages = range(1,2)
    country=''
    body_type=''
    fuel_type=''
    gear_type=''
    url=''
    sub_url=''

    def start_requests(self):
        for k1,v1 in self.countries.items():
            self.country = k1
            for make in self.makes:
                # self.make = make
                for k2, v2 in self.fuel_types.items():
                    # self.fuel_type = v2
                    for k3, v3 in self.body_types.items():
                        # self.body_type = v3
                        for k4, v4 in self.gears.items():
                            # self.gear_type = v4
                            for page in self.pages:
                                self.url=f'https://www.autoscout24.com/lst/{make}?sort=standard&desc=0&gear={k4}&fuel={k2}&ustate=N%2CU&size=20&page={page}&cy={k1}&fregfrom=2005&body={k3}&atype=C&recommended_sorting_based_id=534dfd1e-a110-431b-8892-dc354dc091a6&'
                                # self.url = f'https://www.autoscout24.com/lst/{make}?sort=standard&desc=0&gear={k4}&fuel={k2}&ustate=N%2CU&size=20&page={page}&cy={k1}&fregto=2009&fregfrom=2005&body={k3}&atype=C&recommended_sorting_based_id=534dfd1e-a110-431b-8892-dc354dc091a6&'
                                yield scrapy.Request(
                                    url=self.url,
                                    callback=self.parse
                                )

    def parse(self, response):
        for hrefs in response.xpath("//a[@data-item-name='detail-page-link']"):  #https://docs.scrapy.org/en/latest/topics/selectors.html
            self.sub_url = response.urljoin(hrefs.xpath('.//@href').get())
            yield scrapy.Request(
                url=self.sub_url,
                callback=self.extract_data,
            )

    def extract_data(self, response):

        basic_data={
            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/div/dl/dt[1]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/div/dl/dd[1]/text())").get(),

            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/div/dl/dt[2]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/div/dl/dd[2]/text())").get(),

            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/div/dl/dt[3]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/div/dl/dd[3]/text())").get(),



            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dt[1]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dd[1]/text())").get(),

            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dt[2]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/text())").get(),

            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dt[3]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dd[3]/text())").get(),

            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dt[4]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dd[4]/text())").get(),

            response.xpath(
                "(//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dt[5]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='basic-details-section'])/div/div[2]/div/div[1]/dl/dd[5]/text())").get(),
        }

        vehicle_history={
            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[1]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[1]/text())").get(),

            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[2]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[2]/text())").get(),

            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[3]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[3]/text())").get(),

            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[4]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[4]/text())").get(),

            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[5]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[5]/text())").get(),

            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[6]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[6]/text())").get(),

            response.xpath(
                "(//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dt[7]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='listing-history-section'])/div/div[2]/div/dl/dd[7]/text())").get(),
        }

        technical_data={
            response.xpath(
                "(//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dt[1]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dd[1]/text())").get(),

            response.xpath(
                "(//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dt[2]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/text())").get(),

            response.xpath(
                "(//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dt[3]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dd[3]/text())").get(),

            response.xpath(
                "(//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dt[4]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dd[4]/text())").get(),

            response.xpath(
                "(//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dt[5]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dd[5]/text())").get(),

            response.xpath(
                "(//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dt[6]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='technical-details-section'])/div/div[2]/div/div[1]/dl/dd[6]/text())").get(),

        }

        energy_consumption={
            response.xpath(
                "(//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dt[1]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[1]/text())").get(),

            response.xpath(
                "(//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dt[2]/span/text()").get():
                [response.xpath(
                "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/p[1]/span[1]/text())").get() +" "+
                 response.xpath(
                     "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/p[1]/span[2]/text())").get(),
                 response.xpath(
                     "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/p[2]/span[1]/text())").get()+" "+
                 response.xpath(
                     "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/p[2]/span[2]/text())").get(),
                 response.xpath(
                     "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/p[3]/span[1]/text())").get()+" "+
                 response.xpath(
                     "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[2]/p[3]/span[2]/text())").get(),
                ],

            response.xpath(
                "(//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dt[3]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[3]/text())").get(),

            response.xpath(
                "(//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dt[4]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[4]/text())").get(),

            response.xpath(
                "(//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dt[5]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='environment-details-section'])/div/div[2]/div/div[1]/dl/dd[5]/text())").get(),

        }

        equipment={
            response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dt[1]/span/text()").get(): response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dd[1]/ul").get().rstrip(
                "</li></ul>").lstrip('<ul><li>').split("</li><li>"),

            response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dt[2]/span/text()").get(): response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dd[2]/ul").get().rstrip(
                "</li></ul>").lstrip('<ul><li>').split("</li><li>"),

            response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dt[3]/span/text()").get(): response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dd[3]/ul").get().rstrip(
                "</li></ul>").lstrip('<ul><li>').split("</li><li>"),

            response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dt[4]/span/text()").get(): response.xpath(
                "(//div[@data-cy='equipment-section'])/div/div[2]/div/div[1]/dl/dd[4]/ul").get().rstrip(
                "</li></ul>").lstrip('<ul><li>').split("</li><li>"),

        }

        colour_and_upholstery={
            response.xpath(
                "(//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dt[1]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dd[1]/text())").get(),

            response.xpath(
                "(//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dt[2]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dd[2]/text())").get(),

            response.xpath(
                "(//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dt[3]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dd[3]/text())").get(),

            response.xpath(
                "(//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dt[4]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dd[4]/text())").get(),

            response.xpath(
                "(//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dt[5]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dd[5]/text())").get(),

            response.xpath(
                "(//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dt[6]/span/text()").get(): response.xpath(
                "normalize-space((//div[@data-cy='color-section'])/div/div[2]/div/div[1]/dl/dd[6]/text())").get(),

        }

        yield {
            'location': response.xpath("/html/body/div[1]/div[3]/div/div/main/div[5]/div[2]/a/text()").get(),
            'url': response.url,
            'make': ["\n",response.xpath("(//div[@class='css-11siofd errr7t01'])/span[1]/text()").get(),"\n"],
            'model': ["\n",response.xpath("(//div[@class='css-11siofd errr7t01'])/span[2]/text()").get(),'\n'],
            'short_description': response.xpath("(//div[@class='css-rkx0mf'])/text()").get(),
            'price': [["\n"]+[response.xpath("normalize-space((//span[@class='css-113e8xo'])/text())").get()]+["\n"]],
            'mileage': ['',[response.xpath("(//div[@class='css-esi3fx'])/div/div[4]/text()").get()]],
            'gearbox': ['\n',response.xpath("(//div[@class='css-esi3fx'])/div[2]/div[4]/text()").get(),'\n'],
            'registration': response.xpath("(//div[@class='css-esi3fx'])/div[3]/div[4]/text()").get(),
            'fuel_type': ['\n',response.xpath("(//div[@class='css-esi3fx'])/div[4]/div[4]/text()").get(),'\n'],
            'power': [response.xpath("(//div[@class='css-esi3fx'])/div[5]/div[4]/text()").get(),""],
            'seller': ["\n",[response.xpath("(//div[@class='css-esi3fx'])/div[6]/div[4]/text()").get()+"\n"]],

            # Basic Data
            'body_type': ['\n',basic_data['Body type'] if 'Body type' in basic_data.keys() else 'None','\n'],
            'type':  ['\n',basic_data['Type'] if 'Type' in basic_data.keys() else 'None','\n'],
            'drivetrain':  ['\n',basic_data['Drivetrain'] if 'Drivetrain' in basic_data.keys() else 'None','\n'],
            'seats':  ["\n"+basic_data['Seats'] if 'Seats' in basic_data.keys() else 'None'+"\n"],
            'doors':  ["\n"+basic_data['Doors'] if 'Doors' in basic_data.keys() else 'None'+"\n"],
            'country_version': ["Country version",basic_data['Country version'] if 'Country version' in basic_data.keys() else 'None'],
            'offer_number': '\n'+basic_data['Offer number'] if 'Offer number' in basic_data.keys() else 'None'+"\n",
            'warranty': ['\n',basic_data['Warranty'] if 'Warranty' in basic_data.keys() else 'None','\n'],

            # Vehicle History
            'Mileage': [['\n'],[vehicle_history['Mileage'] if 'Mileage' in vehicle_history.keys() else 'None']],
            'first_registration': vehicle_history['First registration'] if 'First registration' in vehicle_history.keys() else 'None',
            'production_date': vehicle_history['Production date'] if 'Production date' in vehicle_history.keys() else 'None',
            'general_inspection': vehicle_history['General inspection'] if 'General inspection' in vehicle_history.keys() else 'None',
            'last_service': vehicle_history['last_service'] if 'last_service' in vehicle_history.keys() else 'None',
            'full_service_history': ["\n",vehicle_history['Full service history'] if 'Full service history' in vehicle_history.keys() else 'None',"\n"],
            'non_smoker_vehicle': ["\n",vehicle_history['Non-smoker vehicle'] if 'Non-smoker vehicle' in vehicle_history.keys() else 'None','\n'],

            # Technical Data
            'Power': ["\n",technical_data['Power'] if 'Power' in technical_data.keys() else 'None','\n'],
            'Gearbox': ["\n",technical_data['Gearbox'] if 'Gearbox' in technical_data.keys() else 'None','\n'],
            'engine_size': ["\n",technical_data['Engine size'] if 'Engine size' in technical_data.keys() else 'None','\n'],
            'gears': ["\n",technical_data['Gears'] if 'Gears' in technical_data.keys() else 'None','\n'],
            'cylinders': ["\n",technical_data['Cylinders'] if 'Cylinders' in technical_data.keys() else 'None','\n'],
            'empty_weight': ["\n",technical_data['Empty weight'] if 'Empty weight' in technical_data.keys() else 'None','\n'],

            # Energy Consumption
            'Fuel_type': ["\n",energy_consumption['Fuel type'] if 'Fuel type' in energy_consumption.keys() else 'None','\n'],
            'fuel_consumption': ["\n",energy_consumption['Fuel consumption'] if 'Fuel consumption' in energy_consumption.keys() else 'None','\n'],
            'co2_emissions': ["\n",energy_consumption['CO₂-emissions'] if 'CO₂-emissions' in energy_consumption.keys() else 'None','\n'],
            'emission_class': ["\n",energy_consumption['Emission class'] if 'Emission class' in energy_consumption.keys() else 'None','\n'],

            # Equipment
            "\nComfort & Convenience\n": [equipment['Comfort & Convenience'] if 'Comfort & Convenience' in equipment.keys() else 'None'],
            "\nEntertainment & Media\n": [equipment['Entertainment & Media'] if 'Entertainment & Media' in equipment.keys() else 'None'],
            "\nSafety & Security\n": [equipment['Safety & Security'] if 'Safety & Security' in equipment.keys() else 'None'],
            'extras': [equipment['Extras'] if 'Extras' in equipment.keys() else 'None'],

            # Colour and Upholstery
            '\ncolour': ["\n4, "+colour_and_upholstery['Colour'] if 'Colour' in colour_and_upholstery.keys() else 'None'],
            '\nmanufacturer_color': ["\n7, "+colour_and_upholstery['Manufacturer color'] if 'Manufacturer color' in colour_and_upholstery.keys() else 'None'],
            '\npaint': "\npaint, "+colour_and_upholstery['Paint'] if 'Paint' in colour_and_upholstery.keys() else 'None',
            ' upholstery_colour ': "\nupholstery, "+colour_and_upholstery['Upholstery colour'] if 'Upholstery colour' in colour_and_upholstery.keys() else 'None',
            ' upholstery ': "\n8, "+colour_and_upholstery['Upholstery'] if 'Upholstery' in colour_and_upholstery.keys() else 'None',

        }