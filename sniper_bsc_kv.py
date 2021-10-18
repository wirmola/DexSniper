import os, sys
from kivy.resources import resource_add_path, resource_find
from web3 import Web3
import threading
import settings
import datetime
import time
from eth_account import Account
from kivy.app import App
#from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
#from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.widget import Widget
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.properties import StringProperty
#from kivy.core.window import Window




#Window.clearcolor = (0.2, 0.3, 1, 1)


provider_url = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(provider_url))


#PCS_PAIRS:
pcs_bnb_pair  = False
pcs_busd_pair = False
pcs_usdc_pair = False
pcs_usdt_pair = False
pcs_cake_pair = False


private_key = '0x_N0PR1V4T3_K3Y5'

# Deadline for transaction to revert
deadline = int(time.time()) + 85000

# Gas and gas price (BSC Only)
global_gas = 3000000
global_gas_price = web3.toWei(5, 'gwei') #9.69


wbnb = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
busd = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
usdc = '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'
usdt = '0x55d398326f99059fF775485246999027B3197955'
cake = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'

# Pancakeswap Contracts
pcs_router_contract  = web3.eth.contract(address = settings.PCS_router_address, abi = settings.PCS_router_abi)
pcs_factory_contract = web3.eth.contract(address = settings.PCS_factory_address, abi = settings.PCS_factory_abi) 

#Apeswap Contracts




class Main_PCS(GridLayout):

    def pcs_snipe_bnb(self, value, address):
        print(web3.isConnected())
        token_address = web3.toChecksumAddress(address.text)
        buyer = Account.from_key(private_key).address
        print(buyer)
        spend = wbnb

        # Liquidity check starts here
        liquidity_address = pcs_factory_contract.functions.getPair(token_address, wbnb).call()
        # Sometimes the liquidity has not been created and is not zero we need to check again
        if liquidity_address == '0x0000000000000000000000000000000000000000':
            print('Waiting for Liquidity Contract')
            while liquidity_address == '0x0000000000000000000000000000000000000000':
                liquidity_address = pcs_factory_contract.functions.getPair(token_address, wbnb).call()

        liquidity_contract = web3.eth.contract(address= liquidity_address, abi= settings.PCS_pair_abi)
        liquidity_supply = web3.fromWei(liquidity_contract.functions.totalSupply().call(),'ether')

        if liquidity_supply == 0:
            print('waiting for liquidity to be added to contract ...')
            while liquidity_supply == 0:
                liquidity_supply = liquidity_contract.functions.totalSupply().call()
        print(f'Liquidity added : {liquidity_supply} LP-Tokens \n {datetime.datetime.now().strftime("%I:%M:%S %p")}')


        # Optionally check for trading enabled'
        #enabled_trading = contract.functions.tradingEnabled().call()

        #if enabled_trading == False:
        #    print('Waiting for trading to be enabled')
        #    while enabled_trading == False:
        #        enabled_trading = dbubble_contract.functions.tradingEnabled().call()
        
        #print('Trading enabled')
        #↓↓↓↓↓↓
        # HERE
        #↑↑↑↑↑↑
        
        # Buying process starts here
        
    
        #nonce is required to build tx and make sure not multisending.
        
        nonce = web3.eth.get_transaction_count(buyer)

    
            
        tx = pcs_router_contract.functions.swapExactETHForTokens( #swapExactETHForTokensSupportingFeeOnTransferTokens (Optional)
            0, #  ∞ slippage
            [spend, token_address],# Path of tx 
            buyer, # Address that will receive the funds we buy, in this case buyer is also receiver
            deadline
        ).buildTransaction({
            'from': buyer,
            'value': web3.toWei(float(value.text), 'ether'),# BNB amount we swap for
            'gas': global_gas, #it seems if you do not specify the gas, it automatically use an ideal amout of gas
            'gasPrice': global_gas_price,
            'nonce': nonce
        })

        signed_tx  = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (f'Sniped: https://bscscan.com/tx/{web3.toHex(tx_receipt)} @ {datetime.datetime.now().strftime("%I:%M:%S %p")}')

    def pcs_snipe_busd(self, value, address):
        token_address = web3.toChecksumAddress(address.text)
        buyer = Account.from_key(private_key).address
        spend = wbnb

        # Liquidity check starts here
        liquidity_address = pcs_factory_contract.functions.getPair(token_address, busd).call()
        # Sometimes the liquidity has not been created and is not zero we need to check again
        if liquidity_address == '0x0000000000000000000000000000000000000000':
            print('Waiting for Liquidity Contract')
            while liquidity_address == '0x0000000000000000000000000000000000000000':
                liquidity_address = pcs_factory_contract.functions.getPair(token_address, busd).call()

        liquidity_contract = web3.eth.contract(address= liquidity_address, abi= settings.PCS_pair_abi)
        liquidity_supply = web3.fromWei(liquidity_contract.functions.totalSupply().call(),'ether')

        if liquidity_supply == 0:
            print('waiting for liquidity to be added to contract ...')
            while liquidity_supply == 0:
                liquidity_supply = liquidity_contract.functions.totalSupply().call()
        print(f'Liquidity added : {liquidity_supply} LP-Tokens \n {datetime.datetime.now().strftime("%I:%M:%S %p")}')


        # Optionally check for trading enabled'
        #enabled_trading = contract.functions.tradingEnabled().call()

        #if enabled_trading == False:
        #    print('Waiting for trading to be enabled')
        #    while enabled_trading == False:
        #        enabled_trading = dbubble_contract.functions.tradingEnabled().call()
        
        #print('Trading enabled')
        #↓↓↓↓↓↓
        # HERE
        #↑↑↑↑↑↑
        
        # Buying process starts here
        
    
        #nonce is required to build tx and make sure not multisending.
        
        nonce = web3.eth.get_transaction_count(buyer)

    
            
        tx = pcs_router_contract.functions.swapExactETHForTokens( #swapExactETHForTokensSupportingFeeOnTransferTokens (Optional)
            0, #  ∞ slippage
            [spend, busd, token_address],# Path of tx 
            buyer, # Address that will receive the funds we buy, in this case buyer is also receiver
            deadline
        ).buildTransaction({
            'from': buyer,
            'value': web3.toWei(float(value.text), 'ether'),# BNB amount we swap for
            'gas': global_gas, #it seems if you do not specify the gas, it automatically use an ideal amout of gas
            'gasPrice': global_gas_price,
            'nonce': nonce
        })

        signed_tx  = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (f'Sniped: https://bscscan.com/tx/{web3.toHex(tx_receipt)} @ {datetime.datetime.now().strftime("%I:%M:%S %p")}')
    
    def pcs_snipe_usdc(self, value, address):
        
        token_address = web3.toChecksumAddress(address.text)
        buyer = Account.from_key(private_key).address
        spend = wbnb

        # Liquidity check starts here
        liquidity_address = pcs_factory_contract.functions.getPair(token_address, usdc).call()
        # Sometimes the liquidity has not been created and is not zero we need to check again
        if liquidity_address == '0x0000000000000000000000000000000000000000':
            print('Waiting for Liquidity Contract')
            while liquidity_address == '0x0000000000000000000000000000000000000000':
                liquidity_address = pcs_factory_contract.functions.getPair(token_address, usdc).call()

        liquidity_contract = web3.eth.contract(address= liquidity_address, abi= settings.PCS_pair_abi)
        liquidity_supply = web3.fromWei(liquidity_contract.functions.totalSupply().call(),'ether')

        if liquidity_supply == 0:
            print('waiting for liquidity to be added to contract ...')
            while liquidity_supply == 0:
                liquidity_supply = liquidity_contract.functions.totalSupply().call()
        print(f'Liquidity added : {liquidity_supply} LP-Tokens \n {datetime.datetime.now().strftime("%I:%M:%S %p")}')


        # Optionally check for trading enabled'
        #enabled_trading = contract.functions.tradingEnabled().call()

        #if enabled_trading == False:
        #    print('Waiting for trading to be enabled')
        #    while enabled_trading == False:
        #        enabled_trading = dbubble_contract.functions.tradingEnabled().call()
        
        #print('Trading enabled')
        #↓↓↓↓↓↓
        # HERE
        #↑↑↑↑↑↑
        
        # Buying process starts here
        
    
        #nonce is required to build tx and make sure not multisending.
        
        nonce = web3.eth.get_transaction_count(buyer)

    
            
        tx = pcs_router_contract.functions.swapExactETHForTokens( #swapExactETHForTokensSupportingFeeOnTransferTokens (Optional)
            0, #  ∞ slippage
            [spend, usdc, token_address],# Path of tx 
            buyer, # Address that will receive the funds we buy, in this case buyer is also receiver
            deadline
        ).buildTransaction({
            'from': buyer,
            'value': web3.toWei(float(value.text), 'ether'),# BNB amount we swap for
            'gas': global_gas, #it seems if you do not specify the gas, it automatically use an ideal amout of gas
            'gasPrice': global_gas_price,
            'nonce': nonce
        })

        signed_tx  = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (f'Sniped: https://bscscan.com/tx/{web3.toHex(tx_receipt)} @ {datetime.datetime.now().strftime("%I:%M:%S %p")}')
    
    def pcs_snipe_usdt(self, value, address):
        token_address = web3.toChecksumAddress(address.text)
        buyer = Account.from_key(private_key).address
        spend = wbnb

        # Liquidity check starts here
        liquidity_address = pcs_factory_contract.functions.getPair(token_address, usdt).call()
        # Sometimes the liquidity has not been created and is not zero we need to check again
        if liquidity_address == '0x0000000000000000000000000000000000000000':
            print('Waiting for Liquidity Contract')
            while liquidity_address == '0x0000000000000000000000000000000000000000':
                liquidity_address = pcs_factory_contract.functions.getPair(token_address, usdt).call()

        liquidity_contract = web3.eth.contract(address= liquidity_address, abi= settings.PCS_pair_abi)
        liquidity_supply = web3.fromWei(liquidity_contract.functions.totalSupply().call(),'ether')

        if liquidity_supply == 0:
            print('waiting for liquidity to be added to contract ...')
            while liquidity_supply == 0:
                liquidity_supply = liquidity_contract.functions.totalSupply().call()
        print(f'Liquidity added : {liquidity_supply} LP-Tokens \n {datetime.datetime.now().strftime("%I:%M:%S %p")}')


        # Optionally check for trading enabled'
        #enabled_trading = contract.functions.tradingEnabled().call()

        #if enabled_trading == False:
        #    print('Waiting for trading to be enabled')
        #    while enabled_trading == False:
        #        enabled_trading = dbubble_contract.functions.tradingEnabled().call()
        
        #print('Trading enabled')
        #↓↓↓↓↓↓
        # HERE
        #↑↑↑↑↑↑
        
        # Buying process starts here
        
    
        #nonce is required to build tx and make sure not multisending.
        
        nonce = web3.eth.get_transaction_count(buyer)

    
            
        tx = pcs_router_contract.functions.swapExactETHForTokens( #swapExactETHForTokensSupportingFeeOnTransferTokens (Optional)
            0, #  ∞ slippage
            [spend, usdt, token_address],# Path of tx 
            buyer, # Address that will receive the funds we buy, in this case buyer is also receiver
            deadline
        ).buildTransaction({
            'from': buyer,
            'value': web3.toWei(float(value.text), 'ether'),# BNB amount we swap for
            'gas': global_gas, #it seems if you do not specify the gas, it automatically use an ideal amout of gas
            'gasPrice': global_gas_price,
            'nonce': nonce
        })

        signed_tx  = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (f'Sniped: https://bscscan.com/tx/{web3.toHex(tx_receipt)} @ {datetime.datetime.now().strftime("%I:%M:%S %p")}')
    
    def pcs_snipe_cake(self, value, address):
        token_address = web3.toChecksumAddress(address.text)
        buyer = Account.from_key(private_key).address
        spend = wbnb

        # Liquidity check starts here
        liquidity_address = pcs_factory_contract.functions.getPair(token_address, cake).call()
        # Sometimes the liquidity has not been created and is not zero we need to check again
        if liquidity_address == '0x0000000000000000000000000000000000000000':
            print('Waiting for Liquidity Contract')
            while liquidity_address == '0x0000000000000000000000000000000000000000':
                liquidity_address = pcs_factory_contract.functions.getPair(token_address, cake).call()

        liquidity_contract = web3.eth.contract(address= liquidity_address, abi= settings.PCS_pair_abi)
        liquidity_supply = web3.fromWei(liquidity_contract.functions.totalSupply().call(),'ether')

        if liquidity_supply == 0:
            print('waiting for liquidity to be added to contract ...')
            while liquidity_supply == 0:
                liquidity_supply = liquidity_contract.functions.totalSupply().call()
        print(f'Liquidity added : {liquidity_supply} LP-Tokens \n {datetime.datetime.now().strftime("%I:%M:%S %p")}')


        # Optionally check for trading enabled'
        #enabled_trading = contract.functions.tradingEnabled().call()

        #if enabled_trading == False:
        #    print('Waiting for trading to be enabled')
        #    while enabled_trading == False:
        #        enabled_trading = dbubble_contract.functions.tradingEnabled().call()
        
        #print('Trading enabled')
        #↓↓↓↓↓↓
        # HERE
        #↑↑↑↑↑↑
        
        # Buying process starts here
        
    
        #nonce is required to build tx and make sure not multisending.
        
        nonce = web3.eth.get_transaction_count(buyer)

    
            
        tx = pcs_router_contract.functions.swapExactETHForTokens( #swapExactETHForTokensSupportingFeeOnTransferTokens (Optional)
            0, #  ∞ slippage
            [spend, cake, token_address],# Path of tx 
            buyer, # Address that will receive the funds we buy, in this case buyer is also receiver
            deadline
        ).buildTransaction({
            'from': buyer,
            'value': web3.toWei(float(value.text), 'ether'),# BNB amount we swap for
            'gas': global_gas, #it seems if you do not specify the gas, it automatically use an ideal amout of gas
            'gasPrice': global_gas_price,
            'nonce': nonce
        })

        signed_tx  = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (f'Sniped: https://bscscan.com/tx/{web3.toHex(tx_receipt)} @ {datetime.datetime.now().strftime("%I:%M:%S %p")}')

    def sniper(self, amount, token_address):# add value and address and all inherit from it:
        if pcs_bnb_pair == True:
            self.snipe_bnb(amount, token_address)
        elif pcs_busd_pair == True:
            self.snipe_busd(amount, token_address)
        elif pcs_usdc_pair == True:
            self.snipe_usdc(amount, token_address)
        elif pcs_usdt_pair == True:
            self.snipe_usdt(amount, token_address)
        elif pcs_cake_pair == True:
            self.snipe_cake(amount, token_address)
        else:
            print ('Select a pair . . . ')

    def snipe_bnb(self, value, address):
        thread = threading.Thread(target= self.pcs_snipe_bnb, args=[value, address])
        thread.start()
    
    def snipe_busd(self, value, address):
        thread = threading.Thread(target= self.pcs_snipe_busd, args=[value, address])
        thread.start()
    
    def snipe_usdc(self, value, address):
        thread = threading.Thread(target= self.pcs_snipe_usdc, args=[value, address])
        thread.start()
    
    def snipe_usdt(self, value, address):
        thread = threading.Thread(target= self.pcs_snipe_usdt, args=[value, address])
        thread.start()
    
    def snipe_cake(self, value, address):
        thread = threading.Thread(target= self.pcs_snipe_cake, args=[value, address])
        thread.start()
    
class Main_APE(GridLayout):

    def pcs_snipe(self,pk, value, address):
    
        token_address = web3.toChecksumAddress(address.text)
        buyer = Account.from_key(pk.text).address
        print(buyer)
        spend = wbnb

        # Liquidity check starts here
        liquidity_address = pcs_factory_contract.functions.getPair(token_address, wbnb).call()
        # Sometimes the liquidity has not been created and is not zero we need to check again
        if liquidity_address == '0x0000000000000000000000000000000000000000':
            print('Waiting for Liquidity Contract')
            while liquidity_address == '0x0000000000000000000000000000000000000000':
                liquidity_address = pcs_factory_contract.functions.getPair(token_address, wbnb).call()

        liquidity_contract = web3.eth.contract(address= liquidity_address, abi= settings.PCS_pair_abi)
        liquidity_supply = web3.fromWei(liquidity_contract.functions.totalSupply().call(),'ether')

        if liquidity_supply == 0:
            print('waiting for liquidity to be added to contract ...')
            while liquidity_supply == 0:
                liquidity_supply = liquidity_contract.functions.totalSupply().call()
        print(f'Liquidity added : {liquidity_supply} LP-Tokens \n {datetime.datetime.now().strftime("%I:%M:%S %p")}')


        # Optionally check for trading enabled'
        #enabled_trading = contract.functions.tradingEnabled().call()

        #if enabled_trading == False:
        #    print('Waiting for trading to be enabled')
        #    while enabled_trading == False:
        #        enabled_trading = dbubble_contract.functions.tradingEnabled().call()
        
        #print('Trading enabled')
        #↓↓↓↓↓↓
        # HERE
        #↑↑↑↑↑↑
        
        # Buying process starts here
        
    
        #nonce is required to build tx and make sure not multisending.
        
        nonce = web3.eth.get_transaction_count(buyer)

    
            
        tx = pcs_router_contract.functions.swapExactETHForTokens( #swapExactETHForTokensSupportingFeeOnTransferTokens (Optional)
            0, #  ∞ slippage
            [spend, token_address],# Path of tx 
            buyer, # Address that will receive the funds we buy, in this case buyer is also receiver
            deadline
        ).buildTransaction({
            'from': buyer,
            'value': web3.toWei(float(value.text), 'ether'),# BNB amount we swap for
            'gas': global_gas, #it seems if you do not specify the gas, it automatically use an ideal amout of gas
            'gasPrice': global_gas_price,
            'nonce': nonce
        })

        signed_tx  = web3.eth.account.sign_transaction(tx, private_key=pk.text)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (f'Sniped: https://bscscan.com/tx/{web3.toHex(tx_receipt)} @ {datetime.datetime.now().strftime("%I:%M:%S %p")}')

    def snipe(self, pk, value, address):
        thread = threading.Thread(target= self.pcs_snipe, args=[pk, value, address])
        thread.start()


class SettingPage(BoxLayout):

    def set_pk(self, pk):
        global private_key 
        private_key = pk.text

    def set_provider(self, url):
        global provider_url, web3
        provider_url = url.text
        web3 = Web3(Web3.HTTPProvider(provider_url))
    


class SideMenu_PCS(GridLayout):

    def reset_pair_pcs(self):
        global pcs_bnb_pair, pcs_busd_pair, pcs_usdc_pair, pcs_usdt_pair, pcs_cake_pair
        
        pcs_bnb_pair  = False
        pcs_busd_pair = False
        pcs_usdc_pair = False
        pcs_usdt_pair = False
        pcs_cake_pair = False

    def select_pair_BNB(self, btn):
        global pcs_bnb_pair
        self.reset_pair_pcs()
        if btn.state == 'down':
            pcs_bnb_pair = True
        
    def select_pair_BUSD(self, btn):
        global pcs_busd_pair
        self.reset_pair_pcs()
        if btn.state == 'down':
            pcs_busd_pair = True
        
    
    def select_pair_USDC(self, btn):
        global pcs_usdc_pair
        self.reset_pair_pcs()
        if btn.state == 'down':
            pcs_usdc_pair = True
        
    
    def select_pair_USDT(self, btn):
        global pcs_usdt_pair
        self.reset_pair_pcs()
        if btn.state == 'down':
            pcs_usdt_pair = True
        
    
    def select_pair_CAKE(self, btn):
        global pcs_cake_pair
        self.reset_pair_pcs()
        if btn.state == 'down':
            pcs_cake_pair = True
        

class SniperApp(App):
    pass



#SniperApp().run()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    SniperApp().run()