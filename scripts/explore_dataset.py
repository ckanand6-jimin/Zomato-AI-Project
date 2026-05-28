from datasets import load_dataset

ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
print("rows", len(ds))
print("columns", ds.column_names)
print("sample", ds[0])
