class Formatter:

    @staticmethod
    def format_status(status):
        print('--------------------')
        print('Modem Status')
        print('--------------------')
        print('Provider  :', status['providerName'])
        print('Connection:', status['connectionType'])
        print('Signal    :', str(status['signal'] * 100) + '%')
        print('--------------------')

        if len(status['msgs']):
            print('New Messages')
            for msg in status['msgs']:
                print('From:', msg['sender'])
                print('Date:', msg['date'])
                print('Text:', msg['msg'])
                print()
            print('--------------------')
