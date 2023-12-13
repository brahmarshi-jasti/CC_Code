"""This script extracts AWS Spot prices."""

from urllib.request import urlopen
import json
import constants


class GetPriceFromAWS:
    """GetPriceFromAWS class."""

    def __init__(self):
        """Initialize class."""
        self.url = "http://spot-price.s3.amazonaws.com/spot.js"
        # self.df = pd.DataFrame()
        self.cpu = []
        self.cpu_score = []
        self.memory = []
        self.memory_score = []
        self.spot_price = []

    def correct_region(self, region):
        """Correct region function."""
        if region == "us-east":
            region = "us-east-1"
        elif region == "us-west":
            region = "us-west-1"
        elif region == "apac-sin":
            region = "ap-southeast-1"
        elif region == "apac-syd":
            region = "ap-southeast-2"
        elif region == "apac-tokyo":
            region = "ap-northeast-1"
        elif region == "eu-ireland":
            region = "eu-west-1"
        return region

    def correct_os(self, os):
        """Correct os function."""
        if os == "linux":
            os = "Linux"
        elif os == "mswin":
            os = "Windows"
        else:
            print("the os is wrong")
        return os

    def aws_data_extraction(self, ec2, region):
        """Aws_data_extraction function."""
        file_to_read = urlopen(self.url)
        raw_data = file_to_read.read()
        raw_data = raw_data.lstrip(b"callback(").rstrip(b");")
        prices = json.loads(raw_data)
        if region != "all" and not isinstance(region, list):  ##case of one region
            data_region = ec2[region]
            for item in data_region:
                # selecting searching criteria form ec2 file
                os_type = item["os"]
                type_name = item["typeName"]
                # looping through the Prices JSON to find a match
                for ec2_region in prices["config"]["regions"]:
                    # check if the region is matching
                    prices_region = self.correct_region(ec2_region["region"])
                    if prices_region == region:
                        for instance_type in ec2_region["instanceTypes"]:
                            for size in instance_type["sizes"]:
                                # check if the instance type is matching
                                if size["size"].lower() == type_name.lower():
                                    for value in size["valueColumns"]:
                                        # check if the os is matching
                                        os_name = self.correct_os(value["name"])
                                        if os_name == os_type:
                                            index = data_region.index(item)
                                            # updating the item details with spot prices
                                            if isinstance(
                                                value["prices"]["USD"], str
                                            ):  ## check if string
                                                item["spot_price"] = "N/A"
                                                item["Price_per_CPU"] = "N/A"
                                                item["Price_per_memory"] = "N/A"
                                            else:
                                                item["spot_price"] = float(
                                                    value["prices"]["USD"]
                                                )
                                                item["Price_per_CPU"] = float(
                                                    item["spot_price"]
                                                    / float(item["cpu"])
                                                )
                                                item["Price_per_memory"] = float(
                                                    item["spot_price"]
                                                    / float(item["memory"])
                                                )
                                            ec2[region][index] = item
        else:  ##case of multiple regions
            if isinstance(region, list):
                regions = region
            else:
                regions = constants.AWS_REGIONS.copy()
            for region in regions:
                region = self.correct_region(region)
                data_region = ec2[region]
                for item in data_region:
                    # selecting searching criteria form ec2 file
                    os_type = item["os"]
                    type_name = item["typeName"]
                    # looping through the Prices JSON to find a match
                    for ec2_region in prices["config"]["regions"]:
                        # check if the region is matching
                        prices_region = self.correct_region(ec2_region["region"])
                        if prices_region == region:
                            for instance_type in ec2_region["instanceTypes"]:
                                for size in instance_type["sizes"]:
                                    # check if the instance type is matching
                                    if size["size"].lower() == type_name.lower():
                                        for value in size["valueColumns"]:
                                            # check if the os is matching
                                            os_name = self.correct_os(value["name"])
                                            if os_name == os_type:
                                                index = data_region.index(item)
                                                # updating the item details with spot prices
                                                try:
                                                    item["spot_price"] = float(
                                                        value["prices"]["USD"]
                                                    )
                                                    item["Price_per_CPU"] = float(
                                                        item["spot_price"]
                                                        / float(item["cpu"])
                                                    )
                                                    item["Price_per_memory"] = float(
                                                        item["spot_price"]
                                                        / float(item["memory"])
                                                    )
                                                except Exception as e:
                                                    print(e)
                                                    item["spot_price"] = "N/A"
                                                    item["Price_per_CPU"] = "N/A"
                                                    item["Price_per_memory"] = "N/A"
                                                ec2[region][index] = item
        return ec2

    def calculate_spot_price(self, ec2, region):
        """Calculate spot price function."""
        print("Extracting Data from AWS")
        ec2 = self.aws_data_extraction(ec2, region)
        return ec2
