# Zero-Knowledge Proofs (ZKPs)
This repo contains code for the SIEVE/Oracle project (TA1).

ZKPs allow data to be verified without revealing that data. For an overview of how they work, see articles under ["What is a zero-knowledge proof?"](https://zkp.science/)

Our goal is to convert legally, socially, or commercially relevant scenarios into statements and generate constraint systems in an Assembly-like language that conforms to a previously agreed upon standard. Two platforms facilitate the interoperability of "frontend" (ie constraint generators) and "backend" (ie prover/verifier) libraries: zkinterface and wiztoolkit.

## [WizToolKit](https://github.mit.edu/sieve-all/wiztoolkit)
*Repos only available on the MIT Github and not accessible to the general public.*

## [zkinterface](https://github.com/QED-it/zkinterface)

### Installation
1) Install [Rust](https://www.rust-lang.org/tools/install) (also installs Cargo)       
2) Switch to rust-nightly `rustup default nightly`       
3) `source $HOME/.cargo/env`  
4) `cargo install zkinterface`     

### Frontend (Trusted Party)

<table>
<tr>
  <th>Library</th>
  <th>Getting Started</th>
</tr>
<tr></tr>

<tr>
  <td><a href="https://zokrates.github.io/">Zokrates</a></td>
  <td>
  1) <code>curl -LSfs get.zokrat.es | sh</code> <br>  
  2) MacOS: add <code>$HOME/.zokrates/bin</code> to your .bash_profile
  </td>
</tr>
<tr></tr>

<tr>
  <td><a href="https://github.com/meilof/pysnark">pySNARK</a></td>
  <td>
    <pre lang="csharp">
    pip install git+https://github.com/meilof/pysnark <br>
    pip install flatbuffers <br>
    PYSNARK_BACKEND=zkinterface python aggregate_stats/pysnark/main.py
    </pre>
    This will generate a `computation.zkif` file containing the R1CS. To view the file, make sure you've installed Rust nightly (and Cargo) and have clone the
    <a href="https://github.com/QED-it/zkinterface">zkinterface</a> library  
    <pre>
    cd zkinterface/rust/
    cargo run explain path/to/computation.zkif
    </pre>
  </td>
</tr>
<tr></tr>

<tr>
  <td><a href="https://github.com/scipr-lab/libsnark">Libsnark</a></td>
  <td>
  1)  MacOS: add <code> brew install cmake </code> <br>  
  </td>
</tr>

</table>

### Backend (Prover/Verifier)
<table>
<tr>
  <th>Library</th>
  <th>Getting Started</th>
</tr>
<tr></tr>

<tr>
  <td><a href="">Bulletproof</a></td>
  <td>
    <pre lang="csharp">
    git clone https://github.com/QED-it/bulletproofs.git
    cd bulletproofs
    cargo install --features yoloproofs --path .
    </pre>
  </td>
</tr>
<tr></tr>

<tr>
  <td><a href="https://docs.rs/bellman/0.8.0/bellman/">Bellman</a></td>
  <td>
    <pre lang="csharp">
    git clone https://github.com/QED-it/zkinterface-bellman.git
    cd zkinterface-bellman
    cargo install --path .
    </pre>
  </td>
</tr>

</table>
