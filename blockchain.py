import time
import hashlib
import urllib.parse
from urllib.parse import urlparse
import json

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def calc_hash(self):
        # Get SHA256 hash of block

        block_string = json.dumps(self.__dict__, sort_keys=True)
        raw_hash = hashlib.sha256(block_string.encode())
        hex_hash = raw_hash.hexdigest()
        return hex_hash


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    @property
    def last_block(self):
        # Get last block in the chain

        return self.chain[-1]

    @property
    def difficulty(self):
        # Complexity of proof of work algorithm

        return 2

    def create_genesis_block(self):
        # Create the first block in the chain

        genesis_block = Block(
            index = 0,
            timestamp = time.time(),
            transactions = [],
            previous_hash = '0'
        )

        genesis_block.hash = genesis_block.calc_hash()
        self.chain.append(genesis_block)

    def new_transaction(self, sender, recipient, amount):
        # Add transaction to the list

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.pending_transactions.append(transaction)

        return len(self.chain)

    def mine(self):
        # Create new block with pending transactions

        if not self.pending_transactions:
            return False

        block = Block(
            index = len(self.chain),
            timestamp = time.time(),
            transactions = self.pending_transactions,
            previous_hash = self.last_block.calc_hash()
        )

        proof = self.calc_proof(block)
        self.add_block(block, proof)
        self.pending_transactions = []

        return block.index

    def add_block(self, block, proof):
        # Forge block to chain if valid
        
        if block.previous_hash != self.last_block.calc_hash():
            return False

        if not self.validate_proof(block, proof):
            return False

        self.chain.append(block)

        return True

    def calc_proof(self, block):
        # Simple proof of work algorithm - hash must begin with # of zeros defined by difficulty property

        hash = block.calc_hash()

        while not hash.startswith('0' * self.difficulty):
            block.nonce += 1
            hash = block.calc_hash()

        return hash

    def validate_proof(self, block, proof):
        # Validate the hash of a block 

        return (block.calc_hash().startswith('0' * self.difficulty) and block.calc_hash() == proof)

    def validate_chain(self):
        #Compare block hashes to ensure the chain hasn't been tampered with

        for(i in range (2, len(self.chain)):
            current_block = self.chain[i];
            prebious_block = self.chain[i-1];

            if current_block.hash != current_block.calc_hash()
                return False
          
            if current_block.previous_hash != previous_block.hash
                return False

            if not current_block.calc_hash().startswith('0' * self.difficulty):
                return False;

            if not previous_block.calc_hash().startswith('0' * self.difficulty):
                return False;
        
        return True

    def resolve_conflicts(self):
        # Simple consensus algorithm finds longest valid chain