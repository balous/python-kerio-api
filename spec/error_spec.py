from expects import *
import kerio.api

with description(kerio.api.Error):
    with context('both params'):
        with it('formats message'):
            e = kerio.api.Error('501', 'it sucks')

            expect(e.message).to(equal('Http code: 501, json-rpc message: it sucks'))

    with context('no message'):
        with it('formats message'):
            e = kerio.api.Error('501')

            expect(e.message).to(equal('Http code: 501'))
