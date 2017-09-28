# github-amazonSQS-jenkins

プロキシの関係でGithubのWebhookを直接ローカルマシンが受けられなかったので、GithubのWebhookをAmazon SQSに飛ばすようにして、それをローカルから定期的に取りに行ってWebhookがあればJenkinsを実行させるためのスクリプト。

# 使い方
1: ~/.aws/credentialsを作り以下の内容を設定

```
[default]
aws_access_key_id = ABABABABABABABABBABA
aws_secret_access_key = Cd12Cd12Cd12Cd12Cd12
region = ap-northeast-1
```

2: conf.txt.sampleをconf.txtに名前を変えて中身を記述

3: `python get_message.py` を定期実行するようにする

