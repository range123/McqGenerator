from pipelines import pipeline
from typing import Optional
# import spacy
# import neuralcoref

class QuestionGenerator:
    def __init__(self, model_path : str):
        pass
    def generate_questions(self, text : str):
        pass

class QuestionAnswerGenerator:
    def __init__(self, model_path : str):
        pass

    def generate_question_answer(self, text : str):
        pass

class T5QuestionAnswerGenerator(QuestionAnswerGenerator):
    def __init__(self, model_path : str):
       self.model = pipeline('multitask-qa-qg',model=model_path)
    #    self.nlp = spacy.load('en')
    #    neuralcoref.add_to_pipe(self.nlp,greedyness=0.5,max_dist=50,blacklist=False)

    def _preprocess(self, text : str) -> str:
        # TODO : do pronoun resolution
        text = ' '.join(text.split())
        '''For pronoun resolution '''
        # doc = self.nlp(text)
        # print(doc)
        # resolved_coref = doc._.coref_resolved
        # return resolved_coref.lower()

        text = text.lower() # The model seems to internally lowercase the text which causes some indexing issues in the pipeline

        return text

    def generate_question_answer(self, text : str, max_questions : Optional[int] = None):
        preprocessed_text = self._preprocess(text)
        result = self.model(preprocessed_text)
        max_questions = min(max_questions if max_questions else float('inf'), len(result))
        return result[:max_questions]


class T5QuestionGenerator(QuestionGenerator):
    def __init__(self, model_path : str):
        pass
    def generate_questions(self, text : str):
        pass

class BertQuestionAnswerGenerator(QuestionAnswerGenerator):
    def __init__(self, model_path : str):
        pass
    def generate_question_answer(self, text : str):
        pass

if __name__ == "__main__":
    model = T5QuestionAnswerGenerator('../../saved_models/t5-small-qa-qg-hl')
    # text = '''The adjective "deep" in deep learning comes from the use of multiple layers in the network. Early work showed that a linear perceptron cannot be a universal classifier, and then that a network with a nonpolynomial activation function with one hidden layer of unbounded width can on the other hand so be. Deep learning is a modern variation which is concerned with an unbounded number of layers of bounded size, which permits practical application and optimized implementation, while retaining theoretical universality under mild conditions. In deep learning the layers are also permitted to be heterogeneous and to deviate widely from biologically informed connectionist models, for the sake of efficiency, trainability and understandability, whence the "structured" part.'''
    text = '''Deep learning has evolved hand-in-hand with the digital era, which has brought about an explosion of data in all forms and from every region of the world. This data, known simply as big data, is drawn from sources like social media, internet search engines, e-commerce platforms, and online cinemas, among others. This enormous amount of data is readily accessible and can be shared through fintech applications like cloud computing.

    However, the data, which normally is unstructured, is so vast that it could take decades for humans to comprehend it and extract relevant information. Companies realize the incredible potential that can result from unraveling this wealth of information and are increasingly adapting to AI systems for automated support.

    Deep learning unravels huge amounts of unstructured data that would normally take humans decades to understand and process.
    Deep Learning vs. Machine Learning
    One of the most common AI techniques used for processing big data is machine learning, a self-adaptive algorithm that gets increasingly better analysis and patterns with experience or with newly added data.

    If a digital payments company wanted to detect the occurrence or potential for fraud in its system, it could employ machine learning tools for this purpose. The computational algorithm built into a computer model will process all transactions happening on the digital platform, find patterns in the data set, and point out any anomaly detected by the pattern.

    Deep learning, a subset of machine learning, utilizes a hierarchical level of artificial neural networks to carry out the process of machine learning. The artificial neural networks are built like the human brain, with neuron nodes connected together like a web. While traditional programs build analysis with data in a linear way, the hierarchical function of deep learning systems enables machines to process data with a nonlinear approach.

    Electronics maker Panasonic has been working with universities and research centers to develop deep learning technologies related to computer vision.1﻿

    Special Considerations
    A traditional approach to detecting fraud or money laundering might rely on the amount of transaction that ensues, while a deep learning nonlinear technique would include time, geographic location, IP address, type of retailer, and any other feature that is likely to point to fraudulent activity. The first layer of the neural network processes a raw data input like the amount of the transaction and passes it on to the next layer as output. The second layer processes the previous layer’s information by including additional information like the user's IP address and passes on its result.

    The next layer takes the second layer’s information and includes raw data like geographic location and makes the machine’s pattern even better. This continues across all levels of the neuron network.

    A Deep Learning Example
    Using the fraud detection system mentioned above with machine learning, one can create a deep learning example. If the machine learning system created a model with parameters built around the number of dollars a user sends or receives, the deep-learning method can start building on the results offered by machine learning.

    Each layer of its neural network builds on its previous layer with added data like a retailer, sender, user, social media event, credit score, IP address, and a host of other features that may take years to connect together if processed by a human being. Deep learning algorithms are trained to not just create patterns from all transactions, but also know when a pattern is signaling the need for a fraudulent investigation. The final layer relays a signal to an analyst who may freeze the user’s account until all pending investigations are finalized.

    Deep learning is used across all industries for a number of different tasks. Commercial apps that use image recognition, open-source platforms with consumer recommendation apps, and medical research tools that explore the possibility of reusing drugs for new ailments are a few of the examples of deep learning incorporation.

    ARTICLE SOURCES
    Related Terms
    Artificial Neural Network (ANN)
    An artificial neural network (ANN) is the foundation of artificial intelligence (AI), solving problems that would be nearly impossible by humans. more
    Machine Learning
    Machine learning, a field of artificial intelligence (AI), is the idea that a computer program can adapt to new data independently of human action. more
    Reading Into Predictive Modeling
    Predictive modeling is the process of using known results to create, process, and validate a model that can be used to forecast future outcomes. more
    Inside Data Science and Its Applications
    Data science focuses on the collection and application of big data to provide meaningful information in industry, research, and life contexts. more
    Neural Network Definition
    Neural network is a series of algorithms that seek to identify relationships in a data set via a process that mimics how the human brain works. more
    AI Winter Definition
    AI (Artificial Intelligence) winter is a time period in which funding for projects aimed at developing human-like intelligence in machines is minimal. more
    Partner Links
    '''
    print(model.generate_question_answer(text))
