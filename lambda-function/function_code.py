import matplotlib.pyplot as plt
import numpy as np
import json

def main():
    freq = 1
    amp = 1
    x = np.arange(0,4 * np.pi, .1)
    y = np.sin(freq * x ) * amp

    plt.plot(x,y)
    plt.savefig('plot')
    plt.show()

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }