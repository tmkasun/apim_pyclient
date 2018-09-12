def main():
    text = """WSO2 API Publisher enables API providers to publish APIs, share documentation, provision
                                API keys and gather feedback on features, quality and usage. To get started, Create an
                                API or Publish a sample API."""
    encored_text = ""
    for word in text.split(' '):
        encored_text += word.lower() + "."
    print(encored_text)

if __name__ == '__main__':
    main()
