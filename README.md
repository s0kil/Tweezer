<p align="center">
    <img width=100% src="Tweezer.gif">
  </a>
</p>
<p align="center"> 🤖 Binary Analysis, Function Name Finding ⚙️ </b> </p>

<div align="center">

![GitHub contributors](https://img.shields.io/github/contributors/user1342/Tweezer)
![GitHub last commit](https://img.shields.io/github/last-commit/user1342/Tweezer)
<br>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7C2MM6)

</div>

Put simply, Tweezer is a tool for identifying function names in stripped binaries and un-named functions. Using a model/ dataset trained of broad or specific binaries Tweezer can provide a function name for a function that is close to the unamed function - using word2vec and cosine distance.

* **🔬 Function Finding:** Take a function with no name/ unknown functionality and run it through the model. Tweezer will retrieve the names of similar function's it's been trained against.
* **🤖 Specific Training and Extending:** Tweezer is easily extendable and trainable off any binaries supported in Ghidra's decompilation.
* **🛠️ Ghidra Enabled:** Tweezer uses Ghidra headless to enable decompilation of functions!

# ⚙️ Setup

## Dependancies

Tweezer requires [Ghidra](https://ghidra-sre.org/) to be installed, and for ```analyzeHeadless``` to be on your path. If
it is not on your path Tweezer will request on run where the binary is located. To install all other dependancies use
the ```requirements.txt``` file, with:

```
pip install -r requirements.txt
python setup.py install
```

## Running

Depending on if you already have a trained model/ map of vectors you may decide to run Tweezer in one of two ways,
either 1) to train a new model/ extend an existing model or 2) to run Tweezer against a decompiled function or binary. 

An example model for testing can be found in the Github repo at [example_tweezer.mdl](https://github.com/user1342/Tweezer/blob/main/example_tweezer.mdl). This model should not be used in production as it has only been trained off a single binary from [Cisco Talos Binary Function Similarity](https://github.com/Cisco-Talos/binary_function_similarity).

### Training/ Extending the Model
Use this entrypoint when training a new or extending a model. A model file is a pickled list of vectors the word2vec model has outputted. Because of this, existing 'models' can be extended endlessly without the need to start from scratch.
```bash
tweezer --model-path <model-path> --train <binary-folder-1> <binary-folder-2>...
```

### Finding Closest Functions
This entrypoint can be used and pointed to a file on disc that contains the decompilation of a function.
```bash
tweezer --model-path <model-path> --function <path-to-decompiled-function>
```

### Building Function Name Map
This entrypoint can be used to point to a binary on disc to decompile and build a map of all function names against their closest names in the model. **This is the reccomended entrypoint**.
```bash
tweezer --model-path <model-path> --binary <path-to-binary>
```

## Example
Below is an example output when running the aformentioned example model against the unlabelled [7zr binary found hear](https://github.com/polaco1782/linux-static-binaries/tree/master).

```bash
tweezer --model-path example_tweezer.mdl --binary 7zr
```

```
====================
{'FUN_000100f4': ['TS_ACCURACY_get_seconds',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
 'FUN_00010100': ['policy_node_match',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
 'FUN_00010124': ['OCSP_resp_find_status',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
 'FUN_0001014c': ['bn_mul_mont',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
 'FUN_000101d8': ['RSA_padding_check_PKCS1_type_2',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
 'FUN_000102bc': ['X509_NAME_get_index_by_OBJ',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
 'FUN_000102e0': ['RIPEMD160_Transform',
                  'libcrypto.so.1.0.0_TP-Link_Deco-M4_1.0.2d_mips32'],
...
```

# 🤖 What is Word2Vec?
Word2Vec is a widely used technique in natural language processing (NLP) for converting words into dense vectors that
capture semantic relationships between words. The underlying idea is rooted in the distributional hypothesis, which
poses that words appearing in similar contexts tend to have similar meanings. In the context of Tweezer, Word2Vec is
employed to vectorize decompiled code snippets. During the training phase, the model learns to represent words (in this
case, decompiled pseudo C) as vectors in a continuous vector space. These vectors preserve the syntactic and semantic
information of the corresponding words, enabling the model to understand relationships between different functions based
on their co-occurrence patterns. Consequently, when Tweezer encounters a decompiled function, it uses the trained
Word2Vec model to convert the code into vectors. By comparing these vectors (the first 500, and padding if less), Tweezer can identify and retrieve functions
with similar code structures, aiding in the task of finding the closest functions in terms of code similarity.

# 🙏 Contributions

Tweezer is an open-source project and welcomes contributions from the community. If you would like to contribute to
Tweezer, please follow these guidelines:

- Fork the repository to your own GitHub account.
- Create a new branch with a descriptive name for your contribution.
- Make your changes and test them thoroughly.
- Submit a pull request to the main repository, including a detailed description of your changes and any relevant
  documentation.
- Wait for feedback from the maintainers and address any comments or suggestions (if any).
- Once your changes have been reviewed and approved, they will be merged into the main repository.

# ⚖️ Code of Conduct

Tweezer follows the Contributor Covenant Code of Conduct. Please make
sure [to review](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md). and adhere to
this code of conduct when contributing to Tweezer.

# 🐛 Bug Reports and Feature Requests

If you encounter a bug or have a suggestion for a new feature, please open an issue in the GitHub repository. Please
provide as much detail as possible, including steps to reproduce the issue or a clear description of the proposed
feature. Your feedback is valuable and will help improve Tweezer for everyone.

# 📜 License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
