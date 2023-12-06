import pandas as pd
from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
primers_data = {"BU-173": "Bacteria universal", "Lpla-144": "Lactobacillus plantarum", "Laci-85": "Lactobacillus acidophilus", "Lrha-122": "Lactobacillus rhamnosus", "Lpar-80": "Lactobacillus paracasei", "Lgas-329": "Lactobacillus gasseri", "Lhel-87": "Lactobacillus helveticus", "Lreu-93": "Lactobacillus reuteri", "Lbre-369": "Lactobacillus brevis", "Lcas-132": "Lactobacillus casei", "Blon-161": "Bifidobacterium longum", "Bbif-278": "Bifidobacterium bifidum", "Blac-382": "Bifidobacterium lactis", "Bbre-118": "Bifidobacterium breve", "Sthe-114": "Streptococcus thermophilus", "Bado-135": "Bifidobacterium adolescentis", "Lfer-123": "Lactobacillus fermentum", "Bcoa-441": "Bacillus coagulans", "Amun-329": "Akkermansia muciniphila", "Aput-201": "Alistipes putredinis", "Bacg-108": "Bacteroides genus", "Bfra-135": "Bacteroides fragilis", "Bfra-186": "Bacteroides fragilis", "CloIV-242": "Clostridium cluster IV", "Entc-92": "Enterococcus genus", "Esch-204": "Escherichia genus", "Fpra-248": "Faecalibacterium prausnitzii", "Rhom-57": "Roseburia hominis", "Rum-157": "Ruminococcus genus", "Bac-126": "Bacteroidetes phylum", "Fir-200": "Firmicutes phylum", "Bla-339": "Blautia genus", "Robe-314": "Ruminococcus obeum", "Rbro-277": "Ruminococcus bromii", "Calb-273": "Candida albicans", "Ecol-70": "Escherichia coli", "Saur-142": "Staphylococcus aureus", "Baci-111": "Bacillus genus", "Cdif-127": "Clostridioides difficile", "Hpyl-127": "Helicobacter pylori", "Apar-171": "Atopobium parvulum", "Cram-298": "Clostridium ramosum", "Fnuc-112": "Fusobacterium nucleatum", "Gadi-141": "Granulicatella adiacens", "Gmor-300": "Gemella morbillorum", "Lbac-146": "Lachnospiraceae bacterium", "Psto-136": "Peptostreptococcus stomatis", "Sgor-264": "Streptococcus gordonii", "Smoo-452": "Solobacterium moorei", "Svar-65": "Subdoligranulum variabile", "Pgin-143": "Porphyromonas gingivalis", "Tfor-127": "Tannerella forsythia", "Tden-471": "Treponema denticola", "Aact-80": "Aggregatibacter actinomycetemcomitans", "Pint-224": "Prevotella intermedia", "Smut-415": "Streptococcus mutans", "Crec-103": "Campylobacter rectus", "Pnig-276": "Prevotella nigrescens", "Enod-225": "Eubacterium nodatum"}
controls_data = {"NTC": "Negative", "PC": "Positive", "DF": "Positive", "DFP": "Positive", "BU-173PC": "Positive", "Lpla-144PC": "Positive", "Laci-85PC": "Positive", "Lrha-122PC": "Positive", "Lpar-80PC": "Positive", "Lgas-329PC": "Positive", "Lhel-87PC": "Positive", "Lcas-132PC": "Positive", "Lbre-369PC": "Positive", "Lreu-93PC": "Positive", "Blon-161PC": "Positive", "Bbif-278PC": "Positive", "Bbre-118PC": "Positive", "Blac-382PC": "Positive", "Sthe-114PC": "Positive", "Bado-135PC": "Positive", "Lfer-123PC": "Positive", "Bcoa-441PC": "Positive", "Amun-329PC": "Positive", "Aput-201PC": "Positive", "Bacg-108PC": "Positive", "Bfra-135PC": "Positive", "CloIV-242PC": "Positive", "Entc-92PC": "Positive", "Esch-204PC": "Positive", "Fpra-248PC": "Positive", "Rhom-57PC": "Positive", "Rum-157PC": "Positive", "Bac-126PC": "Positive", "Fir-200PC": "Positive", "Bla-339PC": "Positive", "Robe-314PC": "Positive", "Calb-273PC": "Positive", "Ecol-70PC": "Positive", "Rbro-277PC": "Positive", "Saur-142PC": "Positive", "Baci-111PC": "Positive", "Cdif-127PC": "Positive", "Hpyl-127PC": "Positive", "Bang-275PC": "Positive", "Apar-171PC": "Positive", "Cram-298PC": "Positive", "Func-112PC": "Positive", "Gmor-300PC": "Positive", "Gadi-141PC": "Positive", "Lbac-146PC": "Positive", "Psto-136PC": "Positive", "Smoo-452PC": "Positive", "Sgor-264PC": "Positive"}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']
    df = pd.read_excel(file)

    df.columns = df.iloc[12]
    df = df.drop(df.index[0:13], axis=0)

    df.insert(3, 'Controls', '')


    df = df.drop(df.columns[1], axis=1)
    df = df.drop(df.columns[3:7], axis=1)
    df = df.drop(df.columns[4:8], axis=1)
    df = df.drop(df.columns[5:], axis=1)


    df.insert(4, 'Organism Name','')
    df = df.rename(columns={df.columns[0]: 'Well Position',df.columns[1]: 'Sample Name', df.columns[3]: 'Target Name', df.columns[5]: 'CT' })

    df['Controls'] = df['Sample Name'].apply(lambda x: controls_data.get(x, '-'))
    df['Organism Name'] = df['Target Name'].apply(lambda x: primers_data.get(x, '-'))

    output_path = os.path.join('./output/', 'results.xlsx')
    df.to_excel(output_path, index=False)

    return send_from_directory('output', "results.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
