from market.methods import create_order
from symbol.methods import create_symbol, withdraw

CREATE_SYMBOL = 'create_symbol'
CREATE_ORDER = 'create_order'
WITHDRAW = 'withdraw'

METHODS = {
    CREATE_SYMBOL: create_symbol,
    CREATE_ORDER: create_order,
    WITHDRAW: withdraw
}
