from huggingface_hub import hf_hub_download
p = hf_hub_download(
    repo_id='ManikaSaini/zomato-restaurant-recommendation',
    repo_type='dataset',
    filename='zomato.csv',
    revision='5738e9eda2fad49ad51c6e0ed26e761d9b947133',
)
print('DOWNLOADED', p)
