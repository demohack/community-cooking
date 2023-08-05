"""Test forex app"""
from decimal import Decimal
from unittest import TestCase
from app import app
from bs4 import BeautifulSoup

from modules.calc import get_json_data, currency_convert, is_num
from forex_python.converter import CurrencyRates #note: not using the CurrencyCodes, as the service has been unreliable and I found an alternative method using currencies.json file

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

base_url = 'http://127.0.0.1:5000'

class ForexAppTestCase(TestCase):
    """testing Flask app."""

    # on the initial page /, the test is simply whether the elements are present, and we're on the right page
    def test_show_input(self):
        with app.test_client() as client:
            # can now make requests to flask via `client`
            resp = client.get('/', base_url=base_url)
            html = resp.get_data(as_text=True)

            self.assertIn('<h1>FOREX INPUT</h1>', html)

            # import ipdb; ipdb.set_trace()
            soup = BeautifulSoup(html, 'html.parser')

            el = soup.find(id='from_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='to_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='from_amount')
            self.assertNotEqual(el, None)
            el = soup.find(type='submit')
            self.assertNotEqual(el, None)

            el = soup.find(id='not_an_element')
            self.assertEqual(el, None)


    # the edge case for invalid input only happens if user bypasses the input page, e.g. if they use curl or some other method to post directly to the /convert
    # the page will be redirected back to the input page with error message that the input was invalid
    def test_submit_invalid_input(self):
        with app.test_client() as client:
            # import ipdb; ipdb.set_trace()
            resp = client.post('/convert', base_url=base_url,
                               data={'from_currency_code': 'USD', 'to_currency_code': 'GBP', 'from_amount': 'abc'},
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<h1>FOREX INPUT</h1>', html)
            self.assertIn('GBP', html)
            self.assertIn('USD', html)

            soup = BeautifulSoup(html, 'html.parser')

            el = soup.find(id='from_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='to_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='from_amount')
            self.assertNotEqual(el, None)
            el = soup.find(type='submit')
            self.assertNotEqual(el, None)


    # on testing the /convert, we're going to do in two steps, first to not follow redirect, and second step to follow the redirect
    # the redirect on success shows the conversion output page /converted
    # note: ideally we should probably test the amounts and calculation result as well, but not done here
    def test_submit_input(self):
        with app.test_client() as client:
            # import ipdb; ipdb.set_trace()
            resp = client.post('/convert', base_url=base_url,
                               data={'from_currency_code': 'USD', 'to_currency_code': 'GBP', 'from_amount': '100'},
                               follow_redirects=False)

            self.assertEqual(resp.status_code, 302)

            resp = client.post('/convert', base_url=base_url,
                               data={'from_currency_code': 'USD', 'to_currency_code': 'GBP', 'from_amount': '100'},
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<h1>FOREX OUTPUT</h1>', html)
            self.assertIn('GBP', html)
            self.assertIn('USD', html)

            soup = BeautifulSoup(html, 'html.parser')

            from_currency_code = el = soup.find(id='from_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='from_symbol')
            self.assertNotEqual(el, None)
            from_amount = el = soup.find(id='from_amount')
            self.assertNotEqual(el, None)

            to_currency_code = el = soup.find(id='to_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='to_symbol')
            self.assertNotEqual(el, None)
            to_amount = el = soup.find(id='to_amount')
            self.assertNotEqual(el, None)

            try:
                currencyRates = CurrencyRates()
                amount = Decimal(currencyRates.convert(from_currency_code, to_currency_code, from_amount))
            except:
                raw = get_json_data('rates.json')
                rates = raw['data']
                amount = currency_convert(rates, from_currency_code.attrs['value'], to_currency_code.attrs['value'], Decimal(from_amount.attrs['value']))

            self.assertEqual(round(amount,8), round(Decimal(to_amount.attrs['value']),8))

            el = soup.find(type='submit')
            self.assertNotEqual(el, None)


    # testing output page, here we don't care as much on the calculation
    def test_show_output(self):

        with app.test_client() as client:
            #import ipdb; ipdb.set_trace()

            # first setup the conversion
            resp = client.post('/convert', base_url=base_url,
                               data={'from_currency_code': 'USD', 'to_currency_code': 'GBP', 'from_amount': '100'},
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            # then test the converted page

            self.assertEqual(resp.status_code, 200)     #200 request succeeded  #400 bad request  #404 not found
            self.assertIn('GBP', html)
            self.assertIn('USD', html)

            self.assertIn('<h1>FOREX OUTPUT</h1>', html)

            # import ipdb; ipdb.set_trace()
            soup = BeautifulSoup(html, 'html.parser')

            el = soup.find(id='from_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='from_symbol')
            self.assertNotEqual(el, None)
            el = soup.find(id='from_amount')
            self.assertNotEqual(el, None)

            el = soup.find(id='to_currency_code')
            self.assertNotEqual(el, None)
            el = soup.find(id='to_symbol')
            self.assertNotEqual(el, None)
            el = soup.find(id='to_amount')
            self.assertNotEqual(el, None)

            el = soup.find(type='submit')
            self.assertNotEqual(el, None)

