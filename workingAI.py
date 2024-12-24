import requests
from bs4 import BeautifulSoup
import random
import csv
import time
from transformers import BartTokenizer, BartForConditionalGeneration

# Load the BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def generate_summary(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

urls = [
    "https://www.amazon.com/JBL-Tune-510BT-Ear-Headphones/dp/B08WM3LMJF/ref=sr_1_1?crid=12VGDYRF09VOS&dib=eyJ2IjoiMSJ9.d3YLypbaIRr6TW7htNWWsdPJM4ZBZlBQpvG0l1QElBsrnbsCp3sSgrHgRS987LL43Fnf47ytWfppsRo5CL2-e-2AYC2z0OpmENqHXFTIqT7ahRvZH9uzGAcXi1q-0FzJnamt6umCSJqxr3lMBVRQzBD_S2OolPk4qJjYRdZFCgtt7B1cvyXUefpcO_9KjNaLIiv3R7QnLCMjptj1k1FtT3XZTZdXkuMGnFMvPAUuIQo.Wyfzw9u2ne9V9rq7CTpGizWvUZg4WOWggVmYi1oR2Bg&dib_tag=se&keywords=headphones&qid=1734645131&sprefix=headph%2Caps%2C386&sr=8-1",
    "https://www.amazon.com/dp/B0CX1SZPH3/ref=sspa_dk_detail_5?psc=1&pd_rd_i=B0CX1SZPH3&pd_rd_w=xSBfV&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=0G2CNXATN5E0WB3YXC05&pd_rd_wg=sJxi7&pd_rd_r=8ee944a4-f41f-4bc8-8382-4afc70924d17&s=electronics&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM",
    "https://www.amazon.com/Nespresso-Limited-Vertuo-Espresso-DeLonghi/dp/B0DDVMTY88/ref=sr_1_2?dib=eyJ2IjoiMSJ9.iUUvK_AQcCHSzLg0qZzlAYFlVs2LiB_UJ8gy7hRz_cd6ZMRQWF64xnlWnUAS5EavKvGmfFIPUN15k3A5bOY-INAAtEiL5kfWvL9BnF8a7VcYez0Ng10tNBo7KTUgPKM5ZlgPp5DfNGyvhYLbkY5fkO7iOYQmJPmvNmkh6Npg2nl7ETxfbeQUjVhre2rLUaaUqy7cBubIKoVt3Ei5fOPkSJGgx18Kw_xAuhIX5RIFtMOaH_njQhp67Tn1mYQm8NPdOpO5p8ppgle1VJbZo6U2FGZw04ovwRqoAJ0wOm9ze_BzTc1br_aJgXELl8DeJOtK_vHYJPTcDO69HjWCXM5dQt86Xo0oJeZZyYMJGewzmqZZpPCi8TQc_uQ9aMMYvK_UWogmqYimGqasxNGrtrYMExMif7b9tG3X7-wmv50RowNXzNfs1HInJ3Tw3ofzYtpO.z4DFNQpyHJs-C34Ebdne_2EEQxusGkuvKGFOYG0aUyE&dib_tag=se&keywords=nespresso&qid=1734676315&sr=8-2",
    "https://www.amazon.ca/Garmin-Instinct-Smaller-Sized-Elements-Multi-GNSS/dp/B09NMK33N8/ref=pd_ci_mcx_mh_mcx_views_0_image?pd_rd_w=Okpqi&content-id=amzn1.sym.132f1a2b-de6d-4eb4-9982-d6fe080f8827%3Aamzn1.symc.40e6a10e-cbc4-4fa5-81e3-4435ff64d03b&pf_rd_p=132f1a2b-de6d-4eb4-9982-d6fe080f8827&pf_rd_r=9TNDVBGK4NNBPWT4Y305&pd_rd_wg=V5BUX&pd_rd_r=cef7e12e-b4bc-43f2-99ed-33d717a75097&pd_rd_i=B09NMK33N8",
    "https://www.amazon.ca/Botanic-Hearth-Strengthening-Nourishing-Volumizing/dp/B0C6XJMSGP/ref=zg_bs_c_beauty_d_sccl_2/144-6580392-2774417?pd_rd_w=NSbH8&content-id=amzn1.sym.d28d46a2-101c-44f1-978c-068143f1419e&pf_rd_p=d28d46a2-101c-44f1-978c-068143f1419e&pf_rd_r=WQRRTRJ0NVPXYSE69069&pd_rd_wg=CDLCb&pd_rd_r=bed6f2a6-ab19-41b4-b6b0-87e1349a15dd&pd_rd_i=B0C6XJMSGP&psc=1"
]

# List of user agents
useragents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36']

# Headers template
headers_template = {
    "User-Agent": random.choice(useragents),
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}

# Process each URL
for idx, url in enumerate(urls):
    try:
        print(f"Processing URL {idx + 1}: {url}")
        response = requests.get(url, headers=headers_template)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data
        product_data = {}
        product_data["title"] = soup.find('h1', {'id': 'title'}).text.strip() if soup.find('h1', {'id': 'title'}) else None
        
        # Extract product image URL
        product_image_section = soup.find('img', {'id': 'landingImage'})
        if product_image_section:
            product_data["product_image"] = product_image_section['src']
        
        # Extract price
        price_section = soup.find("span", {"class": "a-price"})
        if price_section:
            price = price_section.find("span")
            product_data["price"] = price.text.strip() if price else None
        
        # Extract rating
        rating_section = soup.find("span", {"class": "a-icon-alt"})
        if rating_section:
            product_data["rating"] = rating_section.text.strip()

        # Extract number of ratings
        reviews_section = soup.find("span", {"id": "acrCustomerReviewText"})
        product_data["number_of_ratings"] = reviews_section.text.strip() if reviews_section else "N/A"
        
        # Extract specifications
        specs = soup.find_all("tr", {"class": "a-spacing-small"})
        specs_data = {spec.find_all("span")[0].text.strip(): spec.find_all("span")[1].text.strip() for spec in specs if spec.find_all("span")}
        product_data["specs"] = specs_data
        
        # Extract "About this item" section
        about_section = soup.find("div", {"id": "feature-bullets"})
        if about_section:
            about_items = [item.text.strip() for item in about_section.find_all("span", {"class": "a-list-item"})]
            if about_items:  # Check if there are any items
                product_data["about_this_item"] = generate_summary(" ".join(about_items))  # Summarize extracted items
            else:
                product_data["about_this_item"] = "No information available"
        else:
            product_data["about_this_item"] = "No information available"
            
        # Extract reviews
        reviews = []
        review_section = soup.find_all("div", {"data-hook": "review-collapsed"}, limit=100)  # Limit to first 100 reviews
        for review in review_section:
            review_text = review.find("span")
            if review_text:
                reviews.append(review_text.text.strip())
        
        # Join reviews into a single string
        product_data["reviews"] = generate_summary(". ".join(reviews)) if reviews else "No reviews available"
        
        # Save to CSV
        output_file = f"AImainproduct_data_{idx + 1}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Product Image", "Price", "Rating", "Number of Ratings", "Specifications", "About This Item", "Reviews"])
            writer.writerow([
                product_data["title"],
                product_data["product_image"],
                product_data["price"],
                product_data["rating"],
                product_data["number_of_ratings"],
        "; ".join([f"{k}: {v}" for k, v in specs_data.items()]),
        product_data["about_this_item"],  # This now contains the summarized information
        product_data["reviews"]  # This will now contain the summary of reviews
            ])
        print(f"Data saved to {output_file}")
    
    except Exception as e:
        print(f"Error processing URL {idx + 1}: {e}")
