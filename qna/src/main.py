import argparse

from app import App

def main():
    print("Starting qna...")
    
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--interface", 
        action="store", 
        default="web",
        choices=["web", "cli"],
        help="Select the type of interface to be used by the program. Default: %(default)s")

    argument_parser.add_argument(
        "--model", 
        action="store", 
        default="UniversalEncoder",
        choices=["UniversalEncoder", "BERT", "doc2vec"],
        help="Select the NLP model to be used by the program. Default: %(default)s")
    

    args = argument_parser.parse_args()

    app = App(args.model, args.interface)

    app.start()


if __name__ == "__main__":
    main()
