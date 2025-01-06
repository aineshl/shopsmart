import requests
from bs4 import BeautifulSoup
import random
import json
from transformers import BartTokenizer, BartForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor

# Load the BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def generate_summary(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def calculate_price_factor(price1, price2):
    if price1 >= 2 * price2:
        return 0.8
    elif price1 >= 1.5 * price2:
        return 0.85
    elif price1 >= 1.3 * price2:
        return 0.9
    elif price1 >= 1.2 * price2:
        return 0.95
    else:
        return 1.0
    
def calculate_reliability_factor(num_reviews):
    if num_reviews < 40:
        return 0.8
    elif num_reviews < 100:
        return 0.85
    elif num_reviews < 500:
        return 0.95
    else:
        reliability_factor = 1.0
    
    return max(reliability_factor, 0.1)

def scrape_url(url):
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
    
    headers_template = {
        "User-Agent": random.choice(useragents),
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }

    try:
        response = requests.get(url, headers=headers_template)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_data = {}
        product_data["title"] = soup.find('h1', {'id': 'title'}).text.strip() if soup.find('h1', {'id': 'title'}) else None
        product_image_section = soup.find('img', {'id': 'landingImage'})
        if product_image_section:
            product_data["product_image"] = product_image_section['src']
        price_section = soup.find("span", {"class": "a-price"})
        if price_section:
            price = price_section.find("span")
            if price:
                price_str = price.text.strip()  # e.g., "$24.99"
                price_float = float(price_str.replace('$', '').replace(',', ''))
                product_data["price"] = price_float
        else:
            product_data["price"] = None
        rating_section = soup.find("span", {"class": "a-icon-alt"})
        if rating_section:
            product_data["rating"] = float(rating_section.text.strip().split()[0])
        ratings_section = soup.find("span", {"id": "acrCustomerReviewText"})
        ratings_count = int(ratings_section.text.strip().split()[0].replace(",", "")) if ratings_section else 0
        product_data["number_of_ratings"] = ratings_count

        reliability_factor = calculate_reliability_factor(ratings_count)
        adjusted_rating = reliability_factor * product_data["rating"]
        product_data["adjusted_rating"] = round(adjusted_rating, 1)

        specs = soup.find_all("tr", {"class": "a-spacing-small"})
        specs_data = {spec.find_all("span")[0].text.strip(): spec.find_all("span")[1].text.strip() for spec in specs if spec.find_all("span")}
        product_data["specs"] = specs_data

        about_section = soup.find("div", {"id": "feature-bullets"})
        if about_section:
            about_items = [item.text.strip() for item in about_section.find_all("span", {"class": "a-list-item"})]
            if about_items:
                product_data["about_this_item"] = generate_summary(" ".join(about_items))
            else:
                product_data["about_this_item"] = "No information available"
        else:
            product_data["about_this_item"] = "No information available"

        reviews = []
        review_section = soup.find_all("div", {"data-hook": "review-collapsed"}, limit=100)
        for review in review_section:
            review_text = review.find("span")
            if review_text:
                reviews.append(review_text.text.strip())
        product_data["reviews"] = generate_summary(". ".join(reviews)) if reviews else "No reviews available"

        return product_data
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

def scrape_and_summarize(urls):
    results = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(scrape_url, urls))

    # Handle the case where one or more URLs fail to scrape
    results = [result for result in results if result is not None]
    
    if len(urls) == 2:
        price1 = results[0]["price"]
        price2 = results[1]["price"]

        if price1 < price2:
            price1, price2 = price2, price1

        price_factor = calculate_price_factor(price1, price2)

        if results[0]["price"] == price1:
            results[0]["adjusted_rating"] *= price_factor
            results[0]["adjusted_rating"] = round(results[0]["adjusted_rating"], 1)
        else:
            results[1]["adjusted_rating"] *= price_factor
            results[1]["adjusted_rating"] = round(results[1]["adjusted_rating"], 1)

    return results
