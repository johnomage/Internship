import scrapy
from scrapy.item import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst, Join
# from w3lib.html import remove_tags



def remove_quotations(value):
    return value.strip().replace("“", "").replace("”", "")


def remove_tags(value):
    return [text.strip() for text in value] if isinstance(value, list) else value.strip()



class ItemCleaner(Item):
    _id = Field()

    # author field
    author = Field(
        input_processor = MapCompose(str.strip, remove_quotations),
        output_processor = TakeFirst()
    )
    
    quote_text = Field(
        input_processor = MapCompose(str.strip, remove_quotations),
        output_processor = TakeFirst()
    )

    tags = Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Join(",")
    )

    likes = Field(
        input_prrocessor = MapCompose(remove_quotations),
        output_processor = TakeFirst()
    )


    

