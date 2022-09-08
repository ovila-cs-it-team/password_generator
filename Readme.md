# 🔒️🥷 Super Simple and robust Password Generator 🔒️🥷

## What Is That ? 🙊
> This is a very simple but yet robust way to generate words based password to cognitively memorize faster (temporary) 
> passwords.
> It downloads a given word file, should contain only one word by line. Which is not persistent, 
> the resource will be deleted after the call of the function.
> The file will not be fully buffered for performance purposes. 
> 
> 🚨 The file should contain only one word by line.
> 
> Every word will be capitalized and separate by given separator characters.
> 
> The result will take the following format:
> 
>     [WORD1][SEPARATORS][WORD2][SEPARATORS]...[WORDN][SEPARATORS][SPECIAL_CHARACTER]
> 
> You can specify the URL of the file with `url_dict` argument and provide such file :
> 
> - https://raw.githubusercontent.com/Taknok/French-Wordlist/master/francais.txt
> - https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
> - http://math.oxford.emory.edu/site/math117/probSetAllTogether/words.txt
> - Find some more: https://github.com/dwyl/english-words


## How to Use It ? 🙈
```python
    from strong_easy_2_remember_password import GenerateEasy2RememberPassword

    if __name__ == "__main__":
        print("Here you go 🙈:")
        gen_pwd = GenerateEasy2RememberPassword(
            url_dict="https://raw.githubusercontent.com/Taknok/French-Wordlist/master/francais.txt",
            words=2,
            special_characters=2,
            separator="_",
            min_length=15,
        )
        print(
            gen_pwd.generate
        )
```

## TODO 📃
◻️ Load Config From ini file or Yaml file

◻️ Refactor the 'generate' property.
