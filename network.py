import blockchain
import flask 
from flask import Flask, request
from uuid import uuid4
import json

app = Flask(__name__)

blockchain = blockchain.Blockchain()

node_id = str(uuid4()).replace('-', '')


@app.route('/transactions', methods=['GET'])
def get_transactions():
    if not blockchain.pending_transactions:
        return 'No pending transactions'
        
    return json.dumps(blockchain.pending_transactions)


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that required fields are in post response
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Error: Missing transaction data', 400

    block_index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    return f'Transaction will be added to block {block_index}', 201


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)

    return json.dumps(chain)


@app.route('/mine', methods=['GET'])
def mine():
    result = blockchain.mine()

    if not result:
        return 'No transactions to mine'

    # Reward for mining
    blockchain.new_transaction(
        sender = '0',
        recipient = node_id,
        amount = 1
    )

    return f'Block {result} is mined'


@app.route('/nodes/new', methods=['POST'])
def new_node():
    values = request.get_json()

    nodes = values['nodes']
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.nodes.add(node)

    response = {
        'message': 'New node/s added',
        'total_nodes': len(blockchain.nodes)
    }

    return response, 201


@app.route('/nodes/resolve')
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return response


if __name__ == '__main__':
    app.run()
