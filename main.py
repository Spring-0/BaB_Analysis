import hashlib

terminatingHash = '86728f5fc3bd99db94d3cdaf105d67788194e9701bf95d049ad0e1ee3d004277'
salt = '0000000000000000004d6ec16dafe9d8370958664c1dc422f452892264c59526'

# Generate hash chain by applying SHA256 function, will continue to yield until terminating hash value is met
def genHashChain(hash):
    while hash != terminatingHash:
        yield hash
        hash = hashlib.sha256(hash.encode()).hexdigest()

# Calculates the BaB game ID by counting number of intermediate hash values.
def calcGameId(hash):
    count = 0
    for _ in genHashChain(hash):
        count += 1
        if count > 10e6:
            raise Exception("not part of canonical chain?!")
    return count

# Generate random value to determine output of round
def gameResult(seed):
    nBits = 52 # number of most significant bits to use
    hmac = hashlib.sha256(bytes.fromhex(salt))
    hmac.update(bytes.fromhex(seed))
    r = int(hmac.hexdigest()[:nBits // 4], 16)
    X = r / 2**(nBits) # uniformly distributed in [0; 1)
    X = 99 / (1 - X)
    result = int(X)
    return max(1, result / 100)

if __name__ == "__main__":

    seed = input("Enter the game seed: ")
    gameId = calcGameId(seed)
    for hash in genHashChain(seed):
        print(f"game id {gameId} \t {hash} \t {gameResult(hash):.2f}x")
        gameId -= 1