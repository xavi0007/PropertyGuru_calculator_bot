import requests
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton



class PropertyBot(object):
    def __init__(self, token):
        self.amount = []
        self.token = token
        self.age_1 = 0
        self.age_2 = 0
        self.income_1 = 0
        self.cash_1 = 0
        self.cpf_1 = 0
        self.debt_1 = 0
        self.bot = telepot.Bot(self.token)
        self.looper = True
        self.property_valuation = -1
        self.property_price = -1
        #30 be default, 25 for hdb
        self.loan_tenure = 30
        self.interest_rates = 0.0325
        #2d Maxtrix
        self.num_keyboard =[
                                [InlineKeyboardButton(text='1', callback_data= '1'),
                                InlineKeyboardButton(text='2', callback_data= '2'),
                                InlineKeyboardButton(text='3', callback_data= '3')],
                                
                                [InlineKeyboardButton(text='4', callback_data= '4'),
                                InlineKeyboardButton(text='5', callback_data= '5'),
                                InlineKeyboardButton(text='6', callback_data= '6')],
                                
                                [InlineKeyboardButton(text='8', callback_data= '8'),
                                InlineKeyboardButton(text='9', callback_data='9')],
                                
                                [InlineKeyboardButton(text='0', callback_data='0')
                                # InlineKeyboardButton(text='Back', callback_data='AgeEnter'),
                                ],
                            ]

    def start(self):
        MessageLoop(self.bot, {'chat': self.on_chat_message,
                        'callback_query': self.on_callback_query}).run_as_thread()
        print('Listening ...')
        # Keep the program running.
        while self.looper:
            time.sleep(5)
    
    def stop(self):
        self.looper = False
    
    def reset_values(self):
        self.amount = []
        self.age_1 = 0
        self.age_2 = 0
        self.income_1 = 0
        self.cash_1 = 0
        self.cpf_1 = 0
        self.debt_1 = 0
        self.looper = True
        self.property_valuation = -1
        self.property_price = -1
        self.loan_tenure = 30
        self.interest_rates = 0.0325

    def send(pair, order, stop_order, token):
        #Replace token, chat_id & text variables
        # text = f'A new trade has been placed in {pair} at {order.lmitPrice} with a stop at {stop_order.auxPrice}'
        text = f'A new trade has been placed in {pair} at {order} with a stop at {stop_order}'
        params = {'chat_id': 1821896777, 'text': text, 'parse_mode': 'HTML'}
        resp = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(token), params)
        resp.raise_for_status()

    def calculate_BSD(self, price):
        buyer_stamp_duty = 0
        if price <= 180000 :
            buyer_stamp_duty = price * 0.01
        elif price <= 360000 and price > 180000:
            buyer_stamp_duty = 1800 + ((price-180000) * 0.02)
        elif price <= 1000000 and price > 360000:
            buyer_stamp_duty = 1800 + 3600 + ((price-360000) * 0.03)
        elif price <= 1500000 and price > 1000000:
            buyer_stamp_duty = 1800 + 3600 + 19200 + (price-1000000) * 0.04
        elif price <= 3000000 and price > 1500000:
            buyer_stamp_duty = 1800 + 3600 + 19200 + 20000 + (price-1500000) * 0.05
        elif price > 3000000:
            buyer_stamp_duty = 1800 + 3600 + 19200 + 20000 + (price-3000000) * 0.06

        return buyer_stamp_duty

    def on_chat_message(self,msg):
            
        content_type, chat_type, chat_id = telepot.glance(msg)
        try:
            command = msg['text']
            if command == '/start' or command == "start": 
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='Single Applicant', callback_data='Single')],
                        [InlineKeyboardButton(text='Join Applicant', callback_data='Joint')],
                    ])
                self.reset_values()
                self.bot.sendMessage(chat_id, "Select the following!", reply_markup=keyboard)
            else:
                self.bot.sendMessage(chat_id, "Please press /start to begin") #Make sure that the user gives the correct input(edge checking!)
        except KeyError:
            self.bot.sendMessage(chat_id, "Please press /start to begin")
            


    def on_callback_query(self,msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        # print('Callback Query:', query_id, from_id, query_data)
        # bot.answerCallbackQuery(query_id, text='Got it')
        if query_data == 'Single':
            amount = []
            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='1', callback_data= '1'),
                    InlineKeyboardButton(text='2', callback_data= '2'),
                    InlineKeyboardButton(text='3', callback_data= '3')],
                    [InlineKeyboardButton(text='4', callback_data= '4'),
                    InlineKeyboardButton(text='5', callback_data= '5'),
                    InlineKeyboardButton(text='6', callback_data= '6')],
                    [InlineKeyboardButton(text='7', callback_data= '7'),
                    InlineKeyboardButton(text='8', callback_data= '8'),
                    InlineKeyboardButton(text='9', callback_data='9')],
                    [InlineKeyboardButton(text='0', callback_data='0'),
                    InlineKeyboardButton(text='ENTER', callback_data='AgeEnter')],
            ]) 
            self.bot.sendMessage(from_id, 'Key in your age', reply_markup=num_pad_keyboard)
        elif query_data in ['1','2','3','4','5','6','7','8','9','0', '00', '000']:
            if query_data == '00':
                self.amount.append('0')
                self.amount.append('0')
            elif query_data == '000': 
                self.amount.append('0')
                self.amount.append('0')
                self.amount.append('0')
            else:
                self.amount.append(query_data)
            
            self.bot.sendMessage(from_id, f'{self.amount}')

        elif query_data == 'Joint':
            self.bot.sendMessage(from_id, 'Joint Applicant function not in service yet')
            self.bot.sendMessage(from_id, 'Key in first age')

        #Ask for income after ageenter   
        elif query_data == 'AgeEnter':
            self.age_1 = int(''.join(self.amount))
            self.amount = []
            #TODO: dynamic keyboard not working....
            # keyboard = self.num_keyboard
            # keyboard.append([InlineKeyboardButton(text='Back', callback_data='AgeEnter'),
            #             InlineKeyboardButton(text='ENTER', callback_data='IncomeEnter')])
            
            # num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1', callback_data= '1'),
                InlineKeyboardButton(text='2', callback_data= '2'),
                InlineKeyboardButton(text='3', callback_data= '3')],
                [InlineKeyboardButton(text='4', callback_data= '4'),
                InlineKeyboardButton(text='5', callback_data= '5'),
                InlineKeyboardButton(text='6', callback_data= '6')],
                [InlineKeyboardButton(text='7', callback_data= '7'),
                InlineKeyboardButton(text='8', callback_data= '8'),
                InlineKeyboardButton(text='9', callback_data='9')],
                [InlineKeyboardButton(text='0', callback_data='0'),
                 InlineKeyboardButton(text='00', callback_data='00'),
                 InlineKeyboardButton(text=',000', callback_data='000')],
                [InlineKeyboardButton(text='Back', callback_data='Single'),
                    InlineKeyboardButton(text='ENTER', callback_data='IncomeEnter')],
            ])
            
            self.bot.sendMessage(from_id, f'Age {self.age_1} entered, now enter your income', reply_markup = num_pad_keyboard)
        #Ask for cash after incomeenter
        elif query_data == 'IncomeEnter':
            self.income_1 = int(''.join(self.amount))
            self.amount = []
            self.bot.sendMessage(from_id, f'Income entered {self.income_1}')
            
            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1', callback_data= '1'),
                InlineKeyboardButton(text='2', callback_data= '2'),
                InlineKeyboardButton(text='3', callback_data= '3')],
                [InlineKeyboardButton(text='4', callback_data= '4'),
                InlineKeyboardButton(text='5', callback_data= '5'),
                InlineKeyboardButton(text='6', callback_data= '6')],
                [InlineKeyboardButton(text='7', callback_data= '7'),
                InlineKeyboardButton(text='8', callback_data= '8'),
                InlineKeyboardButton(text='9', callback_data='9')],
                [InlineKeyboardButton(text='0', callback_data='0'),
                 InlineKeyboardButton(text='00', callback_data='00'),
                 InlineKeyboardButton(text=',000', callback_data='000')],
                [InlineKeyboardButton(text='Back', callback_data='AgeEnter'),
                InlineKeyboardButton(text='ENTER', callback_data='CashEnter')],
            ])
            
            self.bot.sendMessage(from_id, f'Age {self.age_1}, income {self.income_1:,} entered, now enter your Cash', reply_markup = num_pad_keyboard)

        #Ask for CPF after CashEnter
        elif query_data == 'CashEnter':
            self.cash_1 = int(''.join(self.amount))
            self.amount = []
            self.bot.sendMessage(from_id, f'Cash entered {self.cash_1}')
            
            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1', callback_data= '1'),
                InlineKeyboardButton(text='2', callback_data= '2'),
                InlineKeyboardButton(text='3', callback_data= '3')],
                [InlineKeyboardButton(text='4', callback_data= '4'),
                InlineKeyboardButton(text='5', callback_data= '5'),
                InlineKeyboardButton(text='6', callback_data= '6')],
                [InlineKeyboardButton(text='7', callback_data= '7'),
                InlineKeyboardButton(text='8', callback_data= '8'),
                InlineKeyboardButton(text='9', callback_data='9')],
                [InlineKeyboardButton(text='0', callback_data='0'),
                 InlineKeyboardButton(text='00', callback_data='00'),
                 InlineKeyboardButton(text=',000', callback_data='000')],
                [InlineKeyboardButton(text='Back', callback_data='IncomeEnter'),
                InlineKeyboardButton(text='ENTER', callback_data='CPFEnter')],
            ])
            
            self.bot.sendMessage(from_id, f'Age {self.age_1}, income {self.income_1:,}, cash {self.cash_1:,} entered, now enter your CPF', reply_markup = num_pad_keyboard)
        
        #Ask for Debt after CPFEnter
        elif query_data == 'CPFEnter':
            self.cpf_1 = int(''.join(self.amount))
            self.amount = []
            self.bot.sendMessage(from_id, f'cpf entered {self.cpf_1}')
            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1', callback_data= '1'),
                InlineKeyboardButton(text='2', callback_data= '2'),
                InlineKeyboardButton(text='3', callback_data= '3')],
                [InlineKeyboardButton(text='4', callback_data= '4'),
                InlineKeyboardButton(text='5', callback_data= '5'),
                InlineKeyboardButton(text='6', callback_data= '6')],
                [InlineKeyboardButton(text='7', callback_data= '7'),
                InlineKeyboardButton(text='8', callback_data= '8'),
                InlineKeyboardButton(text='9', callback_data='9')],
                [InlineKeyboardButton(text='0', callback_data='0'),
                 InlineKeyboardButton(text='00', callback_data='00'),
                 InlineKeyboardButton(text=',000', callback_data='000'),],
                [InlineKeyboardButton(text='Back', callback_data='CashEnter'),
                InlineKeyboardButton(text='ENTER', callback_data='DebtEnter')],
            ])
            
            self.bot.sendMessage(from_id, f'Age {self.age_1}, income {self.income_1:,}, cash {self.cash_1:,}, cpf {self.cpf_1:,} entered, now enter your monthly debt obligations', reply_markup = num_pad_keyboard)

        elif query_data == 'DebtEnter':
            self.debt_1 = int(''.join(self.amount))
            self.amount = []
            self.bot.sendMessage(from_id, f'CPF entered {self.debt_1}')
            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1', callback_data= '1'),
                InlineKeyboardButton(text='2', callback_data= '2'),
                InlineKeyboardButton(text='3', callback_data= '3')],
                [InlineKeyboardButton(text='4', callback_data= '4'),
                InlineKeyboardButton(text='5', callback_data= '5'),
                InlineKeyboardButton(text='6', callback_data= '6')],
                [InlineKeyboardButton(text='7', callback_data= '7'),
                InlineKeyboardButton(text='8', callback_data= '8'),
                InlineKeyboardButton(text='9', callback_data='9')],
                [InlineKeyboardButton(text='0', callback_data='0'),
                 InlineKeyboardButton(text='00', callback_data='00'),
                 InlineKeyboardButton(text=',000', callback_data='000'),],
                [InlineKeyboardButton(text='Back', callback_data='CPFEnter'),
                InlineKeyboardButton(text='ENTER', callback_data='PropertyValuation')],
            ])
            self.bot.sendMessage(from_id, f'Age {self.age_1}, income {self.income_1:,}, cash {self.cash_1:,}, cpf {self.cpf_1:,}, debt {self.debt_1:,} entered, now enter your property valuation', reply_markup = num_pad_keyboard)

        elif query_data == 'PropertyValuation':
            self.property_valuation = int(''.join(self.amount))
            self.amount = []
            self.bot.sendMessage(from_id, f'Property valued at {self.property_valuation}')

            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='1', callback_data= '1'),
                InlineKeyboardButton(text='2', callback_data= '2'),
                InlineKeyboardButton(text='3', callback_data= '3')],
                [InlineKeyboardButton(text='4', callback_data= '4'),
                InlineKeyboardButton(text='5', callback_data= '5'),
                InlineKeyboardButton(text='6', callback_data= '6')],
                [InlineKeyboardButton(text='7', callback_data= '7'),
                InlineKeyboardButton(text='8', callback_data= '8'),
                InlineKeyboardButton(text='9', callback_data='9')],
                [InlineKeyboardButton(text='0', callback_data='0'),
                 InlineKeyboardButton(text='00', callback_data='00'),
                 InlineKeyboardButton(text=',000', callback_data='000')],                 
                [InlineKeyboardButton(text='Back', callback_data='DebtEnter'),
                 InlineKeyboardButton(text='Same Value', callback_data='SAME'),
                InlineKeyboardButton(text='ENTER', callback_data='ChoiceCalculator')],
            ])
            self.bot.sendMessage(from_id, f'Age {self.age_1}, income {self.income_1:,}, cash {self.cash_1:,}, cpf {self.cpf_1:,}, debt {self.debt_1:,} entered, value {self.property_valuation:,}, now enter your property price', reply_markup = num_pad_keyboard)

        elif query_data =="SAME":
            self.property_price = self.property_valuation     
            num_pad_keyboard = InlineKeyboardMarkup(inline_keyboard=[ [InlineKeyboardButton(text='Next', callback_data='ChoiceCalculator')] ])
            self.bot.sendMessage(from_id,'now press next', reply_markup = num_pad_keyboard)
        #COllate property price and sumamrise
        elif query_data == 'ChoiceCalculator':
            if self.property_price < 0:
                self.property_price = int(''.join(self.amount))
            self.amount = []
            self.bot.sendMessage(from_id, f'Property priced at {self.property_price}')
            self.bot.sendMessage(from_id, f'Age {self.age_1}, income {self.income_1:,}, cash {self.cash_1:,}, cpf {self.cpf_1:,}, debt {self.debt_1:,} entered, value {self.property_valuation:,}, price {self.property_price:,}')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        # [InlineKeyboardButton(text='TDSR', callback_data='TDSR')],
                        [InlineKeyboardButton(text='Affordability', callback_data='afford')],
                        [InlineKeyboardButton(text='Total To Pay', callback_data='TotalToPay')],
                    ])
            
            self.bot.sendMessage(from_id, "Select the following!", reply_markup=keyboard)
        #logic
        elif query_data == 'afford':
            
            price = min(self.property_price, self.property_valuation)
            # if self.property_price > self.property_valuation:
            #     principal_price = self.property_price
            # #the price can be less than valuation, if fire sale or something
            # elif self.property_price <= self.property_valuation:
            #     principal_price = self.property_price

            # property_actual_valuation = float(self.property_valuation)
            cash_minimum_downpayment_payable = float(price*0.05)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        # [InlineKeyboardButton(text='TDSR', callback_data='TDSR')],
                        [InlineKeyboardButton(text='Total To Pay', callback_data='TotalToPay')],
                    ])
            

            minimum_downpayment_payable = float(price*0.25)
            if self.cash_1 + self.cpf_1 < minimum_downpayment_payable:                
                if self.cash_1 < cash_minimum_downpayment_payable:
                    required_cash = cash_minimum_downpayment_payable - self.cash_1
                    self.bot.sendMessage(from_id, f'Not enough cash for downpayment to buy this property, requires {required_cash:,.2f} more')
                    self.bot.sendMessage(from_id, f'Try changing some values and calculate again by typing start or choose', reply_markup=keyboard)
                else:
                    required_cash_cpf = minimum_downpayment_payable - (self.cash_1 + self.cpf_1)
                    self.bot.sendMessage(from_id, f'Not enough cash and cpf for downpayment to buy this property, requires {required_cash_cpf:,.2f} more')
                    self.bot.sendMessage(from_id, f'Try changing some values and calculate again by typing start or choose', reply_markup=keyboard)
            
            final_age = self.age_1+self.loan_tenure
            if final_age > 65:
                self.loan_tenure = int(65 - self.age_1)

            #calculate tdsr as well
            tdsr = (self.income_1 - self.debt_1) * 0.55
            
           
            if final_age<=65:
                loan_value = price*0.75
                numerator = price*(self.interest_rates/12 )
                denominator = 1- (1+(self.interest_rates/12))**(-self.loan_tenure*12)
                monthly_mortgage = numerator/denominator
                if monthly_mortgage > tdsr:
                    self.bot.sendMessage(from_id, f'Your LTV is 75%. You are not eligible for the loan of up to {loan_value:,.2f}, with monthly mortgage of {monthly_mortgage:,.2f}')
                    income_required = monthly_mortgage/55 * 100
                    self.bot.sendMessage(from_id, f'Your TDSR is {tdsr:,.2f}, require income of {income_required:,.2f} given same debt obligations' )
                    self.bot.sendMessage(from_id, f'Try changing some values and calculate again by typing start or choose', reply_markup=keyboard)
                else:
                    self.bot.sendMessage(from_id, f'Your LTV is 75%. You are eligible for the loan of up to {loan_value:,.2f}, with monthly mortgage of {monthly_mortgage:,.2f}, you can afford with monthly TDSR of {tdsr:,.2f}', reply_markup=keyboard)
            elif final_age>65:
                # print("55% LTV")
                loan_value = price*0.55
                numerator = price*(self.interest_rates/12 )
                denominator = 1- (1+(self.interest_rates/12))**(-self.loan_tenure*12)
                monthly_mortgage = numerator/denominator
                if monthly_mortgage > tdsr:
                    self.bot.sendMessage(from_id, f'Your LTV is 55%. You are not eligible for the loan of up to {loan_value:,.2f}, with monthly mortgage of {monthly_mortgage:,.2f}')
                    income_required = monthly_mortgage/55 * 100
                    self.bot.sendMessage(from_id, f'Your TDSR is {tdsr:,.2f}. require income of {income_required:,.2f} given same debt obligations')
                    self.bot.sendMessage(from_id, f'Try changing some values and calculate again by typing start or choose', reply_markup=keyboard)
                else:
                    self.bot.sendMessage(from_id, f'Your LTV is 55%. You are eligible for the loan of up to {loan_value:,.2f}, with monthly mortgage of {monthly_mortgage:,.2f}, you can afford with monthly TDSR of {tdsr:,.2f}', reply_markup=keyboard)
    
        elif query_data == 'TotalToPay':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        # [InlineKeyboardButton(text='TDSR', callback_data='TDSR')],
                        [InlineKeyboardButton(text='Affordability', callback_data='afford')],
                    ])
            price = max(self.property_price, self.property_valuation)
                        
            final_age = self.age_1+self.loan_tenure
            if final_age > 65:
                self.loan_tenure = int(65 - self.age_1)

            numerator = price*(self.interest_rates/12)
            denominator = 1- (1+(self.interest_rates/12))**(-self.loan_tenure*12)
            monthly_mortgage = numerator/denominator

            price_with_interest = monthly_mortgage*self.loan_tenure*12
            total_interest_payable = price_with_interest - price

            lawyer_fee = 3000
            agent_fee = price*0.01
            buyer_stamp_duty = self.calculate_BSD(price)
            mcst_deposit = 600*6
            
            total_payable_upfront = float(price) + float(lawyer_fee) + float(buyer_stamp_duty) + float(agent_fee) + float(mcst_deposit)
            total_payable_upfront = float(total_payable_upfront)
            self.bot.sendMessage(from_id, f'Buyer Stamp duty is {buyer_stamp_duty:,.2f}, assumes no ABSD')
            self.bot.sendMessage(from_id, f'Total Upfront cost is {total_payable_upfront:,.2f}, with monthly mortgage of {monthly_mortgage:,.2f} of which {total_interest_payable:,.2f} is interest payable at {self.interest_rates*100:.2f}%', reply_markup=keyboard)