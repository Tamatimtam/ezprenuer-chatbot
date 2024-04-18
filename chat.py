from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk import pos_tag
from difflib import SequenceMatcher

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

# Define responses database
responses = {
    "apa itu himatik?": "HIMATIK adalah singkatan dari Himpunan Mahasiswa Teknologi Informasi dan Komputer. HIMATIK merupakan organisasi mahasiswa di bidang teknologi informasi dan komputer di kampus kita.",
    "kapan himatik didirikan?": "HIMATIK didirikan pada tahun 20XX.",
    "siapa pendiri himatik?": "Pendiri HIMATIK adalah...",
    "apa visi dan misi himatik?": "Visi HIMATIK adalah..., sedangkan misi HIMATIK adalah...",
    "apa saja kegiatan yang diadakan oleh himatik?": "HIMATIK mengadakan berbagai kegiatan seperti seminar, workshop, lomba, dan kegiatan sosial.",
    "bagaimana cara bergabung dengan himatik?": "Untuk bergabung dengan HIMATIK, Anda dapat mengikuti proses pendaftaran yang diumumkan oleh panitia penerimaan anggota baru setiap semester.",
    "apakah himatik membuka pendaftaran anggota baru?": "Ya, HIMATIK membuka pendaftaran anggota baru setiap semester.",
    "apa manfaat bergabung dengan himatik bagi mahasiswa?": "Bergabung dengan HIMATIK dapat memberikan pengalaman baru, peluang untuk mengembangkan diri, serta memperluas jaringan dan relasi di dunia teknologi informasi dan komputer.",
    "dimana kantor himatik berada?": "Kantor HIMATIK berada di...",
    "siapa saja pengurus himatik saat ini?": "Pengurus HIMATIK saat ini adalah...",
    "bagaimana cara menghubungi himatik?": "Anda dapat menghubungi HIMATIK melalui media sosial atau mengunjungi kantor HIMATIK di...",
}

# Function to preprocess user input
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())  # Convert input to lowercase and tokenize
    return ' '.join(tokens)  # Convert tokens back to a string

# Function to calculate similarity between two strings
def similarity(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()

# Route to render the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Route to receive and respond to messages from the user
@app.route('/send-message', methods=['POST'])
def send_message():
    user_input = request.json['message']

    # Preprocess user input
    processed_input = preprocess_input(user_input)
    print (processed_input)

    # Find the most similar response
    max_similarity = 0
    best_response = None
    for key in responses:
        sim = similarity(processed_input, key)
        if sim > max_similarity:
            max_similarity = sim    
            best_response = responses[key]

    # Provide the best response
    if max_similarity >= 0.2:  # Threshold for considering a response
        return jsonify({'message': best_response})
    else:
        return jsonify({'message': "Maaf, saya tidak mengerti pertanyaan Anda."})
    

if __name__ == "__main__":
    app.run(debug=True)
