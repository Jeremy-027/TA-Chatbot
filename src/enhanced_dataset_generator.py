# Enhanced dataset_generator.py
import pandas as pd
import random
from typing import List, Dict
import itertools
import os


class EnhancedFashionDatasetGenerator:
    def __init__(self):
        self.skin_tones = {
            "light": ["cerah", "putih", "kuning langsat"],
            "dark": ["sawo matang", "gelap", "coklat"],
            "neutral": [""],
        }

        self.extended_skin_tones = {
            "very_light": ["sangat cerah", "putih pucat", "kulit putih"],
            "medium": ["sawo matang muda", "kuning kecoklatan", "tan"],
            "very_dark": ["coklat tua", "hitam manis", "kulit gelap"],
        }

        self.genders = {
            "pria": ["pria", "laki-laki", "cowok"],
            "wanita": ["wanita", "perempuan", "cewek"],
            "neutral": [""],
        }

        # Expanded color palettes with more options
        self.color_palettes = {
            "light": {
                "formal": [
                    "navy blue",
                    "charcoal grey",
                    "deep burgundy",
                    "forest green",
                    "royal purple",
                    "midnight blue",
                    "dark plum",
                    "deep emerald",
                    "rich maroon",
                    "deep teal",
                ],
                "casual": [
                    "pastel blue",
                    "mint green",
                    "lavender",
                    "light pink",
                    "powder blue",
                    "sky blue",
                    "soft peach",
                    "lilac",
                    "baby blue",
                    "sage green",
                ],
                "accent": [
                    "rose gold",
                    "silver",
                    "pearl white",
                    "soft pink",
                    "light grey",
                    "champagne",
                    "dusty rose",
                    "platinum",
                    "aqua",
                    "soft coral",
                ],
            },
            "dark": {
                "formal": [
                    "chocolate brown",
                    "olive green",
                    "deep gold",
                    "terracotta",
                    "rust orange",
                    "burnt orange",
                    "rich burgundy",
                    "deep teal",
                    "aubergine",
                    "mustard",
                ],
                "casual": [
                    "bright yellow",
                    "coral",
                    "electric blue",
                    "emerald green",
                    "rich purple",
                    "vibrant red",
                    "hot pink",
                    "cobalt blue",
                    "magenta",
                    "lime green",
                ],
                "accent": [
                    "gold",
                    "bronze",
                    "copper",
                    "bright red",
                    "royal blue",
                    "turquoise",
                    "amber",
                    "jade",
                    "crimson",
                    "bright violet",
                ],
            },
        }

        # Enhanced seasonal colors with more detail
        self.seasonal_colors = {
            "spring": {
                "colors": {
                    "main": [
                        "pastel pink",
                        "mint green",
                        "light yellow",
                        "baby blue",
                        "lavender",
                        "peach",
                        "soft coral",
                        "light aqua",
                        "apricot",
                        "periwinkle",
                        "light lime",
                        "soft azure",
                        "blush pink",
                        "seafoam",
                        "cherry blossom",
                    ],
                    "accent": [
                        "white",
                        "light grey",
                        "cream",
                        "rose gold",
                        "pale gold",
                        "silver",
                        "pearl",
                        "champagne",
                        "soft beige",
                        "opal",
                    ],
                },
                "fabrics": [
                    "katun ringan",
                    "linen",
                    "chiffon",
                    "sifon tipis",
                    "voile",
                    "jersey",
                    "rayon",
                ],
                "patterns": [
                    "floral kecil",
                    "polkadot",
                    "garis tipis",
                    "motif bunga sakura",
                    "paisley kecil",
                    "chevron tipis",
                    "motif bunga peony",
                    "daisy print",
                ],
            },
            "summer": {
                "colors": {
                    "main": [
                        "bright white",
                        "sky blue",
                        "coral",
                        "turquoise",
                        "bright yellow",
                        "sea foam green",
                        "hot pink",
                        "vibrant orange",
                        "neon green",
                        "azure",
                        "tangerine",
                        "lime",
                        "vivid blue",
                        "fuschia",
                        "magenta",
                        "cyan",
                    ],
                    "accent": [
                        "metallic silver",
                        "bright gold",
                        "pearl white",
                        "aqua",
                        "electric blue",
                        "neon pink",
                        "chrome",
                        "bright copper",
                        "sunshine yellow",
                    ],
                },
                "fabrics": [
                    "katun",
                    "linen ringan",
                    "jersey",
                    "rayon",
                    "mesh",
                    "batiste",
                    "seersucker",
                ],
                "patterns": [
                    "tropical",
                    "garis-garis",
                    "tie-dye",
                    "abstrak cerah",
                    "palm print",
                    "bunga besar",
                    "buah-buahan",
                    "geometric cerah",
                    "motif laut",
                ],
            },
            "autumn": {
                "colors": {
                    "main": [
                        "burgundy",
                        "forest green",
                        "rust orange",
                        "mustard yellow",
                        "deep brown",
                        "olive green",
                        "terracotta",
                        "deep purple",
                        "chestnut",
                        "amber",
                        "maroon",
                        "ochre",
                        "burnt sienna",
                        "sage",
                        "mahogany",
                        "cinnamon",
                    ],
                    "accent": [
                        "copper",
                        "bronze",
                        "antique gold",
                        "deep red",
                        "burnished brass",
                        "dark amber",
                        "russet",
                        "patina green",
                        "deep teal",
                    ],
                },
                "fabrics": [
                    "wool",
                    "suede",
                    "corduroy",
                    "flannel",
                    "tweed",
                    "microfiber",
                    "denim tebal",
                    "moleskin",
                    "fleece",
                ],
                "patterns": [
                    "plaid",
                    "motif daun",
                    "kotak-kotak",
                    "abstrak earth tone",
                    "herringbone",
                    "paisley",
                    "argyle",
                    "motif daun maple",
                    "tartan",
                ],
            },
            "winter": {
                "colors": {
                    "main": [
                        "pure white",
                        "navy blue",
                        "black",
                        "charcoal grey",
                        "deep red",
                        "emerald green",
                        "royal blue",
                        "ice blue",
                        "plum",
                        "burgundy",
                        "dark purple",
                        "forest green",
                        "pewter",
                        "midnight blue",
                        "garnet",
                    ],
                    "accent": [
                        "silver",
                        "platinum",
                        "white gold",
                        "deep purple",
                        "sapphire",
                        "ruby red",
                        "deep emerald",
                        "metallic blue",
                        "dark gold",
                        "pine green",
                    ],
                },
                "fabrics": [
                    "wool tebal",
                    "velvet",
                    "cashmere",
                    "kulit",
                    "fur",
                    "quilted fabric",
                    "brocade",
                    "thick knit",
                    "nylon waterproof",
                    "mohair",
                ],
                "patterns": [
                    "solid",
                    "geometris",
                    "metalik",
                    "tweed",
                    "Nordic",
                    "snowflake",
                    "herringbone",
                    "diamond",
                    "houndstooth",
                    "pinstripe",
                ],
            },
        }

        # Greatly expanded seasonal outfit recommendations
        self.seasonal_outfits = {
            "spring": {
                "pria": [
                    "kemeja lengan pendek {color} dengan celana chino dan loafers",
                    "polo shirt {color} dengan celana linen dan sneakers putih",
                    "kemeja {pattern} dengan celana katun dan sepatu canvas",
                    "kaos {color} dengan cardigan ringan dan celana bahan",
                    "kemeja {color} dengan jaket ringan {accent} dan celana chino",
                    "t-shirt {color} dengan overshirt {pattern} dan jeans",
                    "kemeja denim dengan chino {color} dan sepatu boat",
                    "henley shirt {color} dengan celana kargo ringan dan desert boots",
                    "kemeja linen {color} dengan bermuda dan espadrilles",
                    "kaos polo {pattern} dengan celana pendek {color} dan moccasins",
                    "kemeja chambray dengan celana linen {color} dan loafers santai",
                    "kaos {color} dengan jaket bomber ringan dan celana stretch",
                ],
                "wanita": [
                    "dress {pattern} berbahan {fabric} dengan flat shoes",
                    "blus {color} dengan rok midi dan sandal",
                    "kemeja {color} dengan celana kulot dan sepatu slip-on",
                    "jumpsuit {color} dengan wedges",
                    "dress wrap {color} dengan cardigan ringan dan flat sandals",
                    "blus {pattern} dengan celana wide-leg {color} dan mules",
                    "kemeja oversize {color} dengan legging dan sneakers putih",
                    "dress shirt {color} dengan palazzo pants dan sandal platform",
                    "top cropped {color} dengan rok A-line {pattern} dan espadrilles",
                    "blus peasant {color} dengan jeans dan sandal tali",
                    "dress maxi {pattern} dengan denim jacket ringan dan wedges",
                    "atasan boho {color} dengan rok midi {pattern} dan ankle boots rendah",
                ],
            },
            "summer": {
                "pria": [
                    "kaos {color} dengan celana pendek dan sandal",
                    "kemeja {pattern} berbahan {fabric} dengan celana pendek dan espadrilles",
                    "tank top {color} dengan celana pantai dan sandal",
                    "polo shirt {color} dengan bermuda shorts dan boat shoes",
                    "kemeja linen tipis {color} dengan celana pendek {accent} dan sandal kulit",
                    "t-shirt {color} dengan swim shorts dan flip-flops",
                    "kemeja Hawaiian {pattern} dengan chino pendek dan slip-on canvas",
                    "tank top {color} dengan celana pendek jogger dan slides",
                    "kaos tanpa lengan {color} dengan celana pendek cargo dan sandal trekking",
                    "kemeja bowling {pattern} dengan celana pendek linen dan sandal",
                    "henley {color} tanpa lengan dengan celana pendek denim dan espadrilles",
                    "kaos polo breathable {color} dengan celana pendek golf dan sneakers ringan",
                ],
                "wanita": [
                    "dress maxi {pattern} dengan sandal",
                    "crop top {color} dengan rok midi dan flat sandals",
                    "blus tanpa lengan {color} dengan celana pendek",
                    "romper {pattern} dengan sandal gladiator",
                    "sarung pantai {pattern} dengan bikini {color} dan flip-flops",
                    "tank top {color} dengan rok mini dan slide sandals",
                    "tube top {color} dengan celana kulot ringan dan wedges",
                    "off-shoulder dress {color} dengan sandal anyaman",
                    "crop top {pattern} dengan high-waisted shorts dan espadrilles",
                    "halter neck {color} dengan rok wrap {pattern} dan flat sandals",
                    "mini dress {color} tanpa lengan dengan strappy sandals",
                    "bandeau top {color} dengan maxi skirt {pattern} dan sandal bedazzled",
                ],
            },
            "autumn": {
                "pria": [
                    "sweater {color} dengan jeans dan chelsea boots",
                    "kemeja flanel {pattern} dengan chinos dan sepatu boots",
                    "turtleneck {color} dengan blazer dan celana bahan",
                    "jaket kulit dengan kaos {color} dan jeans",
                    "cardigan {color} dengan kemeja {accent} dan chino pants",
                    "pullover {color} dengan kemeja denim dan corduroy pants",
                    "jaket bomber {color} dengan sweater {accent} dan celana cargo",
                    "hoodie {color} dengan jeans dan sneakers boot",
                    "sweater rajut {pattern} dengan celana bahan dan desert boots",
                    "long-sleeve henley {color} dengan vest {accent} dan slim jeans",
                    "jaket trucker dengan turtleneck {color} dan chinos",
                    "quarter-zip pullover {color} dengan celana wool dan oxford shoes",
                ],
                "wanita": [
                    "sweater dress {color} dengan boots tinggi",
                    "turtleneck {color} dengan rok midi dan ankle boots",
                    "blazer {color} dengan sweater dan celana bahan",
                    "kemeja {pattern} dengan cardigan dan jeans",
                    "sweater {color} dengan pencil skirt dan knee-high boots",
                    "turtleneck {color} dengan overall dress dan ankle boots",
                    "kemeja flanel {pattern} dengan legging dan high boots",
                    "sweaterdress {color} dengan stocking tebal dan combat boots",
                    "poncho {pattern} dengan jeans skinny dan booties",
                    "knit top {color} dengan rok suede dan knee boots",
                    "blouse {color} dengan vest {accent} dan celana palazzo",
                    "sweater oversized {color} dengan rok mini dan legging tebal",
                ],
            },
            "winter": {
                "pria": [
                    "mantel panjang {color} dengan sweater dan celana wool",
                    "jaket tebal {color} dengan turtleneck dan celana bahan",
                    "coat {color} dengan syal dan sarung tangan senada",
                    "jaket bomber dengan sweater {color} dan celana tebal",
                    "parka {color} dengan sweater turtleneck {accent} dan jeans tebal",
                    "shearling jacket dengan sweater {color} dan wool pants",
                    "duffle coat {color} dengan cable knit sweater dan celana flannel",
                    "quilted jacket dengan sweater {color} dan corduroy pants",
                    "trench coat {color} dengan scarf {pattern} dan leather gloves",
                    "peacoat {color} dengan chunky sweater {accent} dan wool trousers",
                    "down jacket dengan thermal henley {color} dan snow pants",
                    "fur-lined coat dengan fisherman sweater {color} dan heavyweight jeans",
                ],
                "wanita": [
                    "long coat {color} dengan dress rajut dan boots",
                    "sweater turtleneck {color} dengan rok panjang dan boots",
                    "jaket tebal {color} dengan celana wool dan boots tinggi",
                    "mantel {color} dengan syal {pattern} dan sarung tangan",
                    "puffer coat {color} dengan cable knit sweater dan fleece-lined leggings",
                    "wool coat {color} dengan sweater dress dan over-the-knee boots",
                    "shearling jacket dengan turtleneck {color} dan jeans tebal",
                    "cape coat {color} dengan sweater {accent} dan leather pants",
                    "teddy coat dengan thermal dress {color} dan thigh-high boots",
                    "quilted long jacket dengan knit dress {color} dan furry boots",
                    "parka dengan sweater {color} dan thermal leggings",
                    "faux fur coat {color} dengan turtleneck sweater dan wool skirt",
                ],
            },
        }

        # Expanded seasonal query templates
        self.seasonal_queries = [
            "Apa yang cocok dipakai di {season} untuk {gender}?",
            "Rekomendasi outfit {season} untuk {gender}?",
            "Fashion {season} yang bagus untuk {gender}?",
            "Style yang cocok untuk {season}?",
            "Pakaian yang nyaman untuk {season}?",
            "Outfit {season} yang trendy?",
            "Apa yang sebaiknya dipakai saat {season}?",
            "Rekomendasi warna untuk {season}?",
            "Kombinasi warna yang bagus untuk {season}?",
            "Pattern yang cocok untuk {season}?",
            "Gaya berpakaian yang sesuai untuk {season}?",
            "Pakaian {gender} untuk {season}?",
            "Baju apa yang sebaiknya dipakai pada {season}?",
            "Outfit yang trendy untuk {season}?",
            "Saya {gender} ingin tampil cantik/tampan di {season}, apa sarannya?",
            "Bagaimana tips fashion untuk {season}?",
            "Style {gender} untuk {season}?",
            "Outfit yang cocok untuk {gender} di {season}?",
            "Baju seperti apa yang cocok untuk {season}?",
            "Pakaian untuk {gender} berkulit {skin_tone} di musim {season}?",
            "Rekomendasi pakaian untuk {season} di Indonesia?",
            "Bagaimana paduan warna yang cocok untuk {season}?",
            "Model baju yang lagi trend di {season}?",
            "Referensi outfit untuk {gender} di {season}?",
            "Fashion items yang wajib punya untuk {season}?",
        ]

        # More comprehensive weather-related queries
        self.weather_queries = [
            "Baju apa yang cocok untuk cuaca {weather}?",
            "Outfit untuk hari yang {weather}?",
            "Pakaian yang nyaman di cuaca {weather}?",
            "Rekomendasi pakaian untuk {gender} saat cuaca {weather}?",
            "Style yang sesuai untuk cuaca {weather}?",
            "Pakaian {gender} yang cocok untuk hari {weather}?",
            "Tips fashion untuk cuaca {weather}?",
            "Outfit yang trendy untuk cuaca {weather}?",
            "Baju yang sebaiknya dipakai saat cuaca {weather}?",
            "Pakaian untuk {gender} berkulit {skin_tone} di cuaca {weather}?",
            "Apa yang sebaiknya dipakai saat cuaca sedang {weather}?",
            "Rekomendasi fashion untuk menghadapi cuaca {weather}?",
            "Cara berpakaian yang tepat saat cuaca {weather}?",
            "Apa yang sebaiknya saya pakai hari ini jika cuaca {weather}?",
            "Outfit yang comfortable untuk cuaca {weather}?",
        ]

        # Enhanced weather modifiers
        self.weather_modifiers = {
            "hot": {
                "materials": [
                    "katun",
                    "linen",
                    "breathable",
                    "rayon",
                    "chambray",
                    "seersucker",
                    "jersey ringan",
                    "modal",
                    "bambu",
                    "tencel",
                ],
                "styles": [
                    "loose-fit",
                    "sleeveless",
                    "pendek",
                    "flowy",
                    "oversized",
                    "cut-out",
                    "ventilated",
                    "breathable",
                    "ringan",
                    "tipis",
                ],
            },
            "cold": {
                "materials": [
                    "wol",
                    "fleece",
                    "tebal",
                    "thermal",
                    "down",
                    "cashmere",
                    "merino",
                    "knit",
                    "flannel",
                    "sherpa",
                ],
                "styles": [
                    "berlapis",
                    "lengan panjang",
                    "tertutup",
                    "turtleneck",
                    "insulated",
                    "padded",
                    "high-neck",
                    "hooded",
                    "double-breasted",
                    "quilted",
                ],
            },
            "rainy": {
                "materials": [
                    "waterproof",
                    "anti air",
                    "quick dry",
                    "Gore-Tex",
                    "rubber",
                    "nylon",
                    "vinyl",
                    "water-resistant",
                    "polyester coated",
                    "waxed cotton",
                ],
                "styles": [
                    "tahan air",
                    "tertutup",
                    "berlapis",
                    "hooded",
                    "sealed seams",
                    "high-top",
                    "covered",
                    "drawstring",
                    "adjustable",
                    "dengan hood",
                ],
            },
            "windy": {
                "materials": [
                    "windbreaker",
                    "tahan angin",
                    "denim",
                    "twill",
                    "canvas",
                    "microfiber",
                    "polyester",
                    "ripstop",
                    "leather",
                    "heavy cotton",
                ],
                "styles": [
                    "pas badan",
                    "tertutup",
                    "berlapis",
                    "fitted",
                    "layered",
                    "adjustable cuffs",
                    "dengan tali",
                    "secured",
                    "high collar",
                    "zipped",
                ],
            },
        }

        # Extended color recommendations for different skin tones
        self.extended_color_recommendations = {
            "very_light": {
                "best": [
                    "navy blue",
                    "burgundy",
                    "emerald green",
                    "royal purple",
                    "charcoal gray",
                    "deep teal",
                    "ruby red",
                    "sapphire blue",
                    "hunter green",
                    "aubergine",
                ],
                "avoid": [
                    "neon yellow",
                    "light beige",
                    "pale pastels",
                    "white",
                    "light gray",
                    "pale yellow",
                    "champagne",
                    "ivory",
                    "pale pink",
                    "ash blonde",
                ],
            },
            "light": {
                "best": [
                    "deep blue",
                    "forest green",
                    "plum",
                    "berry tones",
                    "burgundy",
                    "navy",
                    "emerald",
                    "rust",
                    "chocolate brown",
                    "deep purple",
                ],
                "avoid": [
                    "orange-yellow",
                    "bright orange",
                    "beige",
                    "pastel yellow",
                    "mustard",
                    "tan",
                    "khaki",
                    "sand",
                    "camel",
                    "peach",
                ],
            },
            "medium": {
                "best": [
                    "coral",
                    "teal",
                    "warm purple",
                    "olive green",
                    "amber",
                    "turquoise",
                    "deep pink",
                    "warm red",
                    "caramel",
                    "jade",
                ],
                "avoid": [
                    "brown close to skin tone",
                    "muted pastel",
                    "taupe",
                    "dull olive",
                    "muddy brown",
                    "middle tan",
                    "yellowish beige",
                    "muted salmon",
                ],
            },
            "dark": {
                "best": [
                    "bright yellow",
                    "fuchsia",
                    "cobalt blue",
                    "bright orange",
                    "lime green",
                    "hot pink",
                    "turquoise",
                    "royal purple",
                    "emerald",
                    "scarlet",
                ],
                "avoid": [
                    "chocolate brown",
                    "dark navy",
                    "muted earth tones",
                    "deep maroon",
                    "dark olive",
                    "black brown",
                    "dark plum",
                    "charcoal",
                    "dark forest green",
                ],
            },
            "very_dark": {
                "best": [
                    "bright white",
                    "electric blue",
                    "hot pink",
                    "lime green",
                    "Kelly green",
                    "vivid purple",
                    "bright red",
                    "gold",
                    "magenta",
                    "sunny yellow",
                ],
                "avoid": [
                    "dark brown",
                    "deep navy",
                    "black",
                    "eggplant",
                    "deep burgundy",
                    "dark charcoal",
                    "ochre",
                    "midnight blue",
                    "espresso",
                    "rich mahogany",
                ],
            },
        }

        # Greatly expanded query templates
        self.templates = {
            "query_templates": [
                "Apa yang cocok untuk {occasion} untuk {gender} berkulit {skin_tone}?",
                "Rekomendasi pakaian {occasion} untuk {gender} dengan kulit {skin_tone}?",
                "Pakaian untuk {occasion}?",
                "Outfit untuk {occasion}?",
                "Apa yang sebaiknya dipakai untuk {occasion}?",
                "Baju untuk {occasion}?",
                "Bagaimana cara berpakaian untuk {gender} berkulit {skin_tone} ke {occasion}?",
                "Outfit yang bagus untuk {gender} dengan kulit {skin_tone} ke {occasion}?",
                "Saya {gender} berkulit {skin_tone} mau pergi ke {occasion}, sebaiknya pakai apa ya?",
                "{gender} berkulit {skin_tone} mau ke {occasion}, enaknya pakai baju apa?",
                "Rekomendasi style untuk {gender} dengan kulit {skin_tone} ke {occasion}?",
                "Apa yang sebaiknya saya kenakan sebagai {gender} berkulit {skin_tone} untuk {occasion}?",
                "Fashion tips untuk {gender} berkulit {skin_tone} untuk {occasion}?",
                "Gaya berpakaian apa yang cocok untuk {gender} berkulit {skin_tone} untuk {occasion}?",
                "Padu padan baju untuk {gender} berkulit {skin_tone} ke {occasion}?",
                "Setelan yang cocok untuk {gender} berkulit {skin_tone} ke {occasion}?",
                "Warna yang cocok untuk {gender} berkulit {skin_tone} untuk {occasion}?",
                "Sebagai {gender} dengan kulit {skin_tone} bagaimana outfit untuk {occasion}?",
                "Rekomendasi untuk {gender} dengan tone kulit {skin_tone} ke {occasion}?",
                "Style apa yang cocok untuk {gender} untuk pergi ke {occasion} dengan kulit {skin_tone}?",
                "Mau ke {occasion}, apa rekomendasi pakaian untuk {gender} berkulit {skin_tone}?",
                "Apa saja item fashion yang cocok untuk {gender} berkulit {skin_tone} untuk {occasion}?",
                "Bagaimana model pakaian yang bagus untuk {gender} berkulit {skin_tone} ke {occasion}?",
                "Saran outfit untuk {gender} untuk acara {occasion} dengan warna kulit {skin_tone}?",
                "Pakaian apa yang akan membuat {gender} berkulit {skin_tone} terlihat bagus di {occasion}?",
                "Tips fashion untuk {gender} dengan kulit {skin_tone} yang akan menghadiri {occasion}?",
                "Outfit yang sesuai untuk {gender} berkulit {skin_tone} menghadiri {occasion}?",
                "Kombinasi pakaian yang cocok untuk {gender} berkulit {skin_tone} untuk ke {occasion}?",
                "Saya akan pergi ke {occasion}, apa yang harus saya pakai sebagai {gender} dengan kulit {skin_tone}?",
                "Bagaimana berpakaian dengan tepat untuk {gender} dengan warna kulit {skin_tone} ke {occasion}?",
            ],
            "occasions": {
                # Formal Categories - Light Skin
                "formal_pria_light": {
                    "events": [
                        "interview kerja",
                        "rapat formal",
                        "seminar bisnis",
                        "presentasi perusahaan",
                        "acara kantoran",
                        "meeting dengan klien",
                        "konferensi bisnis",
                        "seminar profesional",
                        "acara perusahaan",
                        "presentasi proyek",
                        "wawancara profesional",
                        "acara bisnis",
                        "ceremonial kantor",
                        "acara formal kantor",
                        "forum bisnis",
                        "pitch ke investor",
                    ],
                    "responses": [
                        "kenakan setelan jas navy blue dengan kemeja putih dan sepatu pantofel hitam",
                        "kombinasikan blazer gelap dengan kemeja light blue dan celana bahan",
                        "pilih setelan jas charcoal gray dengan kemeja crisp white dan dasi maroon slim",
                        "kenakan jas navy dengan kemeja light blue dan dasi patterned subtil",
                        "padukan blazer biru tua dengan kemeja putih dan celana wool abu-abu",
                        "gunakan setelan jas hitam dengan kemeja berwarna pastel dan dasi senada",
                        "kenakan blazer terstruktur dengan kemeja oxford dan celana chino formal",
                        "pilih setelan three-piece dengan warna deep navy dan aksesoris silver",
                        "padukan kemeja formal putih dengan jas abu-abu dan pocket square berwarna",
                        "kombinasikan blazer navy dengan kemeja stripe tipis dan celana wool",
                    ],
                    "label": 0,
                    "gender": "pria",
                    "skin_tone": "light",
                },
                # Expanded entries for other categories...
                "formal_wanita_light": {
                    "events": [
                        "interview kerja wanita",
                        "rapat formal wanita",
                        "seminar wanita",
                        "presentasi kerja",
                        "conference profesional",
                        "meeting bisnis",
                        "acara formal kantor",
                        "pertemuan dengan klien",
                        "event korporat",
                        "pitching ide",
                        "wawancara posisi manajerial",
                        "forum bisnis wanita",
                    ],
                    "responses": [
                        "kenakan blazer dengan rok pensil dan sepatu heels",
                        "padukan blus formal dengan celana bahan dan flat shoes formal",
                        "pilih dress shift formal dengan blazer cropped dan pumps medium",
                        "kenakan setelan pansuit navy dengan blus silk dan heels classic",
                        "gunakan kemeja crisp dengan pencil skirt dan pointed toe pumps",
                        "padukan blus bow-tie dengan straight-leg trousers dan block heels",
                        "kenakan dress wrap formal dengan blazer slim-cut dan slingback heels",
                        "kombinasikan blus satin dengan wide-leg pants dan sepatu oxford wanita",
                        "gunakan kemeja button-up dengan A-line skirt midi dan heels elegant",
                        "pilih blus sutra dengan celana cigarette dan sepatu loafer formal",
                    ],
                    "label": 1,
                    "gender": "wanita",
                    "skin_tone": "light",
                },
                # Formal Categories - Dark Skin
                "formal_pria_dark": {
                    "events": [
                        "presentasi formal",
                        "seminar bisnis",
                        "meeting executive",
                        "wawancara pekerjaan",
                        "forum diskusi formal",
                        "konferensi industri",
                        "acara corporate",
                        "pitching project",
                        "networking formal",
                        "presentasi ke stakeholder",
                        "diskusi panel",
                        "rapat direksi",
                    ],
                    "responses": [
                        "gunakan setelan jas abu-abu dengan dasi merah dan sepatu pantofel hitam",
                        "kenakan blazer hitam dengan kemeja putih dan celana bahan gelap",
                        "pilih setelan jas berwarna royal blue dengan kemeja putih dan dasi gold",
                        "padukan blazer burgundy dengan kemeja putih dan celana formal hitam",
                        "kenakan setelan double-breasted berwarna deep green dengan accessory gold",
                        "gunakan kemeja turtleneck di bawah blazer structured dengan celana bahan",
                        "kombinasikan jas olive green dengan kemeja cream dan dasi textured",
                        "kenakan blazer deep brown dengan kemeja light blue dan celana wool gelap",
                        "pilih setelan jas dengan pattern subtle dan kemeja solid-color",
                        "padukan kemeja mandarin-collar dengan blazer slim-fit dan celana formal",
                    ],
                    "label": 2,
                    "gender": "pria",
                    "skin_tone": "dark",
                },
                "formal_wanita_dark": {
                    "events": [
                        "acara formal wanita",
                        "rapat formal wanita",
                        "presentasi bisnis",
                        "wawancara eksekutif",
                        "konferensi profesional",
                        "meeting formal",
                        "seminar industri",
                        "event networking",
                        "acara perusahaan formal",
                        "bertemu klien penting",
                        "diskusi panel wanita",
                        "forum profesional",
                    ],
                    "responses": [
                        "gunakan setelan blazer pastel dengan rok midi dan sepatu hak tinggi",
                        "kenakan dress formal dengan warna gelap dan aksesoris minimalis",
                        "pilih blazer bright-colored dengan celana tailored dan pointed heels",
                        "padukan blus jewel-toned dengan pencil skirt dan stiletto heels",
                        "kenakan dress sheath dengan warna vibrant dan classic pumps",
                        "gunakan setelan pansuit dengan blus kontras dan statement jewelry",
                        "pilih dress wrap formal dengan blazer structured dan ankle strap heels",
                        "kenakan kemeja silk dengan wide-leg trousers dan block heels elegant",
                        "padukan blazer gem-toned dengan A-line skirt dan heels classic",
                        "gunakan blus dengan detail menarik, celana cigarette, dan mule heels",
                    ],
                    "label": 3,
                    "gender": "wanita",
                    "skin_tone": "dark",
                },
                # Casual Categories - Light Skin
                "kasual_pria_light": {
                    "events": [
                        "jalan-jalan santai",
                        "hangout",
                        "nongkrong casual",
                        "acara weekend",
                        "gathering informal",
                        "jalan-jalan di mall",
                        "nonton bioskop",
                        "kumpul dengan teman",
                        "acara santai",
                        "jalan-jalan sore",
                        "piknik",
                        "BBQ with friends",
                        "casual day out",
                    ],
                    "responses": [
                        "kenakan kaos dengan jeans dan sneakers casual",
                        "padukan kemeja casual dengan chino pants dan sepatu sneakers",
                        "gunakan kaos polo dengan celana pendek dan slip-on shoes",
                        "padukan henley shirt dengan jeans slim-fit dan sneakers low-top",
                        "kenakan t-shirt graphic dengan celana cargo dan canvas shoes",
                        "gunakan kemeja chambray dengan chino shorts dan boat shoes",
                        "padukan kaos polos dengan celana jogger dan sneakers stylish",
                        "kenakan overshirt dengan kaos basic dan jeans relaxed-fit",
                        "gunakan kaos longline dengan track pants dan sneakers chunky",
                        "padukan kaos vintage dengan celana denim dan slip-on vans",
                    ],
                    "label": 4,
                    "gender": "pria",
                    "skin_tone": "light",
                },
                "kasual_wanita_light": {
                    "events": [
                        "jalan-jalan santai wanita",
                        "nongkrong casual",
                        "hang out with friends",
                        "weekend brunch",
                        "shopping day",
                        "coffee date",
                        "movie night",
                        "casual gathering",
                        "mall day",
                        "piknik wanita",
                        "garden party casual",
                        "afternoon tea",
                        "casual social event",
                    ],
                    "responses": [
                        "kenakan dress casual dengan flat shoes nyaman",
                        "padukan kaos dengan rok A-line dan sneakers",
                        "gunakan blus loose-fit dengan mom jeans dan slip-on shoes",
                        "kenakan t-shirt dengan cullotes dan platform sandals",
                        "padukan tank top dengan rok midi dan white sneakers",
                        "gunakan oversized sweater dengan legging dan ankle boots",
                        "kenakan blus flowy dengan jeans boyfriend dan loafers casual",
                        "padukan kaos crop dengan high-waisted jeans dan sandal flat",
                        "gunakan jumpsuit casual dengan sneakers colorful",
                        "kenakan cardigan panjang dengan kaos dan skinny jeans",
                    ],
                    "label": 5,
                    "gender": "wanita",
                    "skin_tone": "light",
                },
                # Casual Categories - Dark Skin
                "kasual_pria_dark": {
                    "events": [
                        "jalan santai pria",
                        "nongkrong di kafe",
                        "weekend hangout",
                        "casual meetup",
                        "jalan-jalan di taman",
                        "nonton konser",
                        "hangout malam",
                        "kumpul santai",
                        "olahraga casual",
                        "street food hunting",
                        "city walk",
                        "informal dinner",
                    ],
                    "responses": [
                        "gunakan t-shirt hitam dengan jeans biru dan sneakers putih",
                        "padukan polo shirt dengan celana pendek khaki dan sandal santai",
                        "kenakan kaos graphic dengan jogger pants dan sneakers colorful",
                        "gunakan kemeja casual dengan jeans distressed dan chunky sneakers",
                        "padukan tank top dengan overlay shirt dan cargo shorts",
                        "kenakan kaos oversize dengan track pants dan slip-on casual",
                        "gunakan t-shirt dengan print bold dan celana pendek denim",
                        "padukan kaos varsity dengan sweatpants dan high-top sneakers",
                        "kenakan kemeja resort dengan celana linen casual dan espadrilles",
                        "gunakan jersey casual dengan jeans relaxed dan sneakers trendy",
                    ],
                    "label": 6,
                    "gender": "pria",
                    "skin_tone": "dark",
                },
                "kasual_wanita_dark": {
                    "events": [
                        "jalan-jalan wanita",
                        "nongkrong malam wanita",
                        "casual brunch",
                        "weekend getaway",
                        "mall day",
                        "hang out with friends",
                        "coffee shop date",
                        "casual dinner",
                        "movie night out",
                        "taman hiburan",
                        "jalan-jalan sore",
                        "weekend activities",
                    ],
                    "responses": [
                        "kombinasikan blouse casual dengan celana jeans dan sepatu flat",
                        "gunakan dress maxi dengan warna cerah dan sandal nyaman",
                        "kenakan crop top dengan high-waisted pants dan chunky sneakers",
                        "padukan graphic tee dengan rok mini dan platform sandals",
                        "gunakan jumpsuit casual dengan belt statement dan white sneakers",
                        "kenakan off-shoulder top dengan wide-leg pants dan wedges casual",
                        "padukan tank top dengan kimono dan boyfriend jeans",
                        "gunakan t-shirt oversize sebagai dress dengan cycling shorts dan boots",
                        "kenakan tube top dengan palazzo pants dan flat sandals",
                        "padukan halter top dengan denim skirt dan espadrilles",
                    ],
                    "label": 7,
                    "gender": "wanita",
                    "skin_tone": "dark",
                },
                # General Event Categories
                "wedding": {
                    "events": [
                        "pernikahan",
                        "resepsi nikah",
                        "wedding party",
                        "akad nikah",
                        "garden wedding",
                        "pesta pernikahan formal",
                        "destination wedding",
                        "indoor wedding",
                        "outdoor wedding",
                        "pesta pernikahan adat",
                        "wedding dinner",
                        "acara resepsi",
                    ],
                    "responses": [
                        "kenakan gaun panjang dengan heels dan clutch bag",
                        "padukan kebaya modern dengan rok panjang dan selop",
                        "gunakan suit formal dengan dasi dan pocket square senada",
                        "kenakan dress cocktail midi dengan statement jewelry dan stilettos",
                        "padukan blazer dengan dress shirt, celana formal dan oxford shoes",
                        "gunakan long dress dengan detail sequin dan strappy heels",
                        "kenakan tuxedo formal dengan bow tie dan patent leather shoes",
                        "padukan atasan brokat dengan rok A-line panjang dan heels block",
                        "gunakan three-piece suit dengan tie clip dan dress shoes",
                        "kenakan dress tea-length dengan lace overlay dan slingback heels",
                    ],
                    "label": 8,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "party": {
                    "events": [
                        "pesta ulang tahun",
                        "party malam",
                        "cocktail party",
                        "house party",
                        "pesta dansa",
                        "gala dinner",
                        "launch party",
                        "pesta year-end",
                        "celebration party",
                        "pesta kebun",
                        "club night",
                        "pesta formal",
                        "pesta semi-formal",
                    ],
                    "responses": [
                        "kenakan dress party dengan aksesoris berkilau",
                        "padukan kemeja fancy dengan celana formal",
                        "gunakan little black dress dengan statement heels dan clutch",
                        "kenakan blazer velvet dengan kemeja silk dan slim pants",
                        "padukan sequin top dengan rok midi dan ankle-strap heels",
                        "gunakan jumpsuit elegant dengan belt dan platform shoes",
                        "kenakan button-up shirt dengan pattern bold dan chinos premium",
                        "padukan crop top dengan high-waisted pants dan stiletto heels",
                        "gunakan kemeja silk dengan detail menarik dan celana tailored",
                        "kenakan dress bodycon dengan accessories statement dan pumps",
                    ],
                    "label": 9,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "business_meeting": {
                    "events": [
                        "rapat bisnis",
                        "konferensi bisnis",
                        "meeting dengan client",
                        "presentasi project",
                        "diskusi professional",
                        "board meeting",
                        "business lunch",
                        "corporate dinner",
                        "pitching session",
                        "meeting investor",
                        "diskusi kontrak",
                        "pertemuan stakeholder",
                    ],
                    "responses": [
                        "gunakan setelan jas abu-abu dengan kemeja putih",
                        "kombinasikan blazer navy dengan celana bahan hitam",
                        "kenakan blazer structured dengan blus silk dan pencil skirt",
                        "gunakan pansuit dengan kemeja button-up dan pumps classic",
                        "padukan kemeja non-iron dengan celana wool dan belt leather",
                        "kenakan dress sheath dengan blazer slim dan kitten heels",
                        "gunakan setelan jas dengan dasi slim dan cufflinks subtle",
                        "padukan blus bow-neck dengan straight-leg pants dan loafers elegant",
                        "kenakan kemeja oxford dengan jas two-button dan leather shoes",
                        "gunakan dress midi formal dengan cardigan structured dan pumps",
                    ],
                    "label": 10,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                # Weather Categories
                "hot_weather": {
                    "events": [
                        "cuaca panas",
                        "musim kemarau",
                        "hari yang terik",
                        "summer day",
                        "pantai",
                        "poolside",
                        "hari yang gerah",
                        "tropical weather",
                        "outdoor activity",
                        "liburan panas",
                        "summer vacation",
                        "aktivitas luar ruangan panas",
                    ],
                    "responses": [
                        "kenakan pakaian berbahan katun yang menyerap keringat",
                        "gunakan kaos lengan pendek dengan celana pendek",
                        "pilih dress ringan berbahan breathable dengan sandal flat",
                        "kenakan kemeja linen loose-fit dengan celana pendek ringan",
                        "gunakan tank top dengan rok maxi berbahan tipis dan ringan",
                        "padukan t-shirt dengan celana capri katun dan sandal",
                        "kenakan sleeveless top dengan linen pants dan slide sandals",
                        "gunakan polo shirt breathable dengan chino shorts dan slip-ons",
                        "kenakan romper berbahan rayon dengan sandal strappy",
                        "gunakan dress tanpa lengan berbahan sifon dengan flat espadrilles",
                    ],
                    "label": 11,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "cold_weather": {
                    "events": [
                        "cuaca dingin",
                        "musim dingin",
                        "winter holiday",
                        "cuaca berkabut",
                        "mountain retreat",
                        "highland trip",
                        "foggy morning",
                        "autumn day",
                        "winter vacation",
                        "alpine weather",
                        "winter evening",
                        "morning frost",
                    ],
                    "responses": [
                        "kenakan sweater tebal dengan celana panjang",
                        "gunakan pakaian berlapis dengan mantel hangat",
                        "pilih turtleneck dengan lapisan jaket dan syal wool",
                        "kenakan long sleeve thermal dengan outer jacket dan beanie",
                        "gunakan sweatshirt tebal dengan celana jeans lined dan boots",
                        "padukan sweater knit dengan tights tebal dan knee-high boots",
                        "kenakan hoodie dengan jaket puffer dan sarung tangan",
                        "gunakan cardigan wool dengan inner thermal dan celana wool blend",
                        "kenakan coat panjang dengan inner sweater dan syal cashmere",
                        "gunakan jaket sherpa-lined dengan fleece pants dan boots insulated",
                    ],
                    "label": 12,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "rainy_weather": {
                    "events": [
                        "cuaca hujan",
                        "gerimis",
                        "monsoon season",
                        "hujan deras",
                        "light shower",
                        "musim hujan",
                        "rainy day",
                        "winter rain",
                        "outdoor in rain",
                        "drizzle",
                        "stormy weather",
                        "continuous rain",
                    ],
                    "responses": [
                        "kenakan jas hujan dengan sepatu anti air",
                        "gunakan jaket waterproof dengan celana panjang",
                        "pilih raincoat dengan hoodie dan wellington boots",
                        "kenakan waterproof parka dengan water-resistant pants dan rain boots",
                        "gunakan hoodie water-repellent dengan jeans dan waterproof shoes",
                        "padukan lightweight raincoat dengan celana quick-dry dan sneakers waterproof",
                        "kenakan packable rain jacket dengan celana yang tidak menyerap air",
                        "gunakan poncho dengan celana yang cepat kering dan boots karet",
                        "kenakan windbreaker anti-air dengan celana chino dan shoes waterproof",
                        "gunakan jaket dengan sealed seams, celana anti air, dan boots tinggi",
                    ],
                    "label": 13,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "windy_weather": {
                    "events": [
                        "cuaca berangin",
                        "angin kencang",
                        "windy day",
                        "coastal weather",
                        "gunung berangin",
                        "seaside walk",
                        "day at the coast",
                        "outdoor windy",
                        "spring winds",
                        "autumn breeze",
                        "gusty weather",
                        "beachside day",
                    ],
                    "responses": [
                        "kenakan jaket windbreaker dengan celana panjang",
                        "gunakan pakaian berlapis dengan jaket tahan angin",
                        "pilih windproof jacket dengan hoodie dan celana pas badan",
                        "kenakan light scarf dengan jaket berkerah tinggi dan slim jeans",
                        "gunakan topi dengan tali dan jaket dengan adjustable cuffs",
                        "padukan lightweight jacket dengan celana straight-leg dan ankle boots",
                        "kenakan wind-resistant coat dengan inner layer dan celana fitted",
                        "gunakan zipped hoodie dengan celana stretch dan sneakers tertutup",
                        "kenakan layered tops dengan jaket denim dan celana yang tidak kedodoran",
                        "gunakan pullover hoodie dengan jaket denim dan celana skinny",
                    ],
                    "label": 14,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                # Season Categories
                "summer": {
                    "events": [
                        "musim panas",
                        "liburan musim panas",
                        "summer days",
                        "summer trip",
                        "summer evening",
                        "summer beach day",
                        "summer vacation",
                        "summer party",
                        "poolside day",
                        "summer festival",
                        "summer outdoor",
                        "summer garden party",
                    ],
                    "responses": [
                        "kenakan kaos ringan dengan celana pendek dan sandal",
                        "gunakan pakaian berwarna cerah dengan bahan breathable",
                        "pilih sundress dengan strappy sandals dan wide-brim hat",
                        "kenakan lightweight shirt dengan linen shorts dan boat shoes",
                        "gunakan tank top dengan bermuda shorts dan slip-on sandals",
                        "padukan crop top dengan high-waisted shorts dan gladiator sandals",
                        "kenakan linen shirt dengan chino shorts dan espadrilles",
                        "gunakan halter dress dengan flat sandals dan statement sunglasses",
                        "kenakan muscle tee dengan swim shorts dan flip flops",
                        "gunakan off-shoulder top dengan denim shorts dan strappy sandals",
                    ],
                    "label": 15,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "winter": {
                    "events": [
                        "musim dingin",
                        "liburan musim dingin",
                        "winter day",
                        "winter vacation",
                        "winter evening",
                        "winter formal",
                        "snowy day",
                        "winter holiday",
                        "winter outdoor",
                        "ski trip",
                        "winter getaway",
                        "winter night out",
                    ],
                    "responses": [
                        "kenakan jaket tebal dengan celana wool",
                        "gunakan mantel dengan syal dan sepatu boots",
                        "pilih parka dengan inner sweater dan thermal pants",
                        "kenakan turtleneck dengan sweater overlay dan jaket tebal",
                        "gunakan layered clothing dengan wool coat dan gloves",
                        "padukan down jacket dengan celana tebal dan snow boots",
                        "kenakan sweater rajut dengan jaket shearling dan syal tebal",
                        "gunakan puffer coat dengan inner thermal dan winter boots",
                        "kenakan wool peacoat dengan sweater turtleneck dan boots lined",
                        "gunakan hoodie tebal dengan jaket quilted dan sarung tangan knit",
                    ],
                    "label": 16,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "spring": {
                    "events": [
                        "musim semi",
                        "awal musim semi",
                        "spring day",
                        "spring picnic",
                        "spring garden party",
                        "spring outdoor",
                        "spring festival",
                        "spring evening",
                        "spring morning",
                        "spring wedding",
                        "spring brunch",
                        "spring casual day",
                    ],
                    "responses": [
                        "kenakan dress floral dengan cardigan ringan",
                        "gunakan blus dengan rok midi dan flat shoes",
                        "pilih light sweater dengan jeans dan ankle boots",
                        "kenakan kemeja pastel dengan chinos dan loafers",
                        "gunakan light knit top dengan culotte pants dan ballet flats",
                        "padukan denim jacket dengan floral dress dan white sneakers",
                        "kenakan cotton shirt dengan celana linen dan slip-on shoes",
                        "gunakan blus lightweight dengan A-line skirt dan sandal low",
                        "kenakan pullover tipis dengan straight leg pants dan loafers",
                        "gunakan bomber jacket ringan dengan t-shirt dan slim jeans",
                    ],
                    "label": 17,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "autumn": {
                    "events": [
                        "musim gugur",
                        "suasana gugur",
                        "autumn day",
                        "fall season",
                        "autumn picnic",
                        "autumn evening",
                        "autumn outdoor",
                        "autumn festival",
                        "fall gathering",
                        "autumn weekend",
                        "autumn morning",
                        "fall day out",
                    ],
                    "responses": [
                        "kenakan sweater rajut dengan celana panjang",
                        "padukan jaket kulit dengan jeans dan boots",
                        "pilih light turtleneck dengan corduroy pants dan ankle boots",
                        "kenakan flannel shirt dengan jeans dan chelsea boots",
                        "gunakan knit dress dengan legging dan knee-high boots",
                        "padukan denim jacket dengan sweater dan straight-leg jeans",
                        "kenakan cardigan panjang dengan basic top dan slim pants",
                        "gunakan lightweight sweater dengan plaid skirt dan booties",
                        "kenakan quilted vest dengan long-sleeve henley dan chinos",
                        "gunakan suede jacket dengan turtleneck dan boot cut jeans",
                    ],
                    "label": 18,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                # Other Categories
                "other": {
                    "events": [
                        "acara lainnya",
                        "kegiatan umum",
                        "general activity",
                        "special occasion",
                        "everyday activity",
                        "social gathering",
                        "custom event",
                        "multi-purpose",
                        "miscellaneous activity",
                        "general purpose",
                        "special request",
                        "unique occasion",
                    ],
                    "responses": [
                        "gunakan pakaian yang nyaman dan sesuai situasi",
                        "pilih pakaian casual atau formal tergantung kebutuhan",
                        "kenakan outfit yang versatile dan bisa disesuaikan",
                        "gunakan basic pieces yang bisa di-mix and match",
                        "padukan atasan netral dengan bawahan yang adjustable",
                        "kenakan smart casual outfit yang bisa dinaikkan atau diturunkan formalitasnya",
                        "gunakan layered clothing yang bisa disesuaikan dengan situasi",
                        "pilih outfit basic dengan aksesoris yang bisa dimodifikasi",
                        "kenakan pakaian dengan warna netral yang cocok untuk berbagai acara",
                        "gunakan capsule wardrobe items yang bisa dipadukan untuk berbagai kesempatan",
                    ],
                    "label": 19,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
            },
        }

    def generate_variation(
        self, template: str, occasion: str, gender: str, skin_tone: str
    ) -> str:
        """Generate variations of queries with different wordings"""
        gender_term = random.choice(self.genders[gender]) if gender != "neutral" else ""
        skin_tone_term = (
            random.choice(self.skin_tones[skin_tone]) if skin_tone != "neutral" else ""
        )
        if gender == "neutral" and skin_tone == "neutral":
            return f"Apa yang cocok untuk {occasion}?"

        return template.format(
            occasion=occasion, gender=gender_term, skin_tone=skin_tone_term
        )

    def generate_color_recommendation(self, skin_tone: str, occasion_type: str) -> str:
        """Generate specific color recommendations based on skin tone and occasion"""
        if skin_tone in ["light", "dark"]:
            colors = self.color_palettes[skin_tone]
            if "formal" in occasion_type.lower():
                recommended_colors = colors["formal"]
                accent_colors = colors["accent"]
            else:
                recommended_colors = colors["casual"]
                accent_colors = colors["accent"]

            main_color = random.sample(recommended_colors, 2)
            accent_color = random.sample(accent_colors, 1)[0]

            return f" Warna yang sangat cocok untuk Anda adalah {main_color[0]}, {main_color[1]}. Sebaiknya hindari warna yang kurang flattering untuk tone kulit Anda."
        return ""

    def generate_seasonal_dataset(
        self, samples_per_category: int = 100
    ) -> pd.DataFrame:
        """Generate a dataset focused on seasonal fashion recommendations"""
        dataset = []
        seasons = ["spring", "summer", "autumn", "winter"]

        # Fixed seasonal queries that don't require skin_tone parameter
        seasonal_queries = [
            "Apa yang cocok dipakai di {season} untuk {gender}?",
            "Rekomendasi outfit {season} untuk {gender}?",
            "Fashion {season} yang bagus untuk {gender}?",
            "Style yang cocok untuk {season}?",
            "Pakaian yang nyaman untuk {season}?",
            "Outfit {season} yang trendy?",
            "Apa yang sebaiknya dipakai saat {season}?",
            "Rekomendasi warna untuk {season}?",
            "Kombinasi warna yang bagus untuk {season}?",
            "Pattern yang cocok untuk {season}?",
            "Gaya berpakaian yang sesuai untuk {season}?",
            "Pakaian {gender} untuk {season}?",
            "Baju apa yang sebaiknya dipakai pada {season}?",
            "Outfit yang trendy untuk {season}?",
            "Bagaimana tips fashion untuk {season}?",
            "Style {gender} untuk {season}?",
            "Outfit yang cocok untuk {gender} di {season}?",
            "Baju seperti apa yang cocok untuk {season}?",
            "Rekomendasi pakaian untuk {season} di Indonesia?",
            "Bagaimana paduan warna yang cocok untuk {season}?",
            "Model baju yang lagi trend di {season}?",
            "Referensi outfit untuk {gender} di {season}?",
            "Fashion items yang wajib punya untuk {season}?",
        ]

        for season in seasons:
            for gender in ["pria", "wanita", "neutral"]:
                for _ in range(samples_per_category):
                    # Create season-specific query
                    template = random.choice(seasonal_queries)

                    # Handle gender neutral queries
                    if gender == "neutral":
                        template = template.replace("{gender}", "")
                        query = template.format(season=season)
                    else:
                        gender_term = random.choice(self.genders[gender])
                        query = template.format(season=season, gender=gender_term)

                    # Get season data
                    season_data = self.seasonal_colors[season]

                    # Select a random outfit recommendation
                    if gender != "neutral":
                        outfit_options = self.seasonal_outfits[season][gender]
                        base_outfit = random.choice(outfit_options)
                    else:
                        # For neutral, randomly choose between male and female outfits
                        gender_choice = random.choice(["pria", "wanita"])
                        outfit_options = self.seasonal_outfits[season][gender_choice]
                        base_outfit = random.choice(outfit_options)

                    # Select random colors and patterns
                    main_color = random.choice(season_data["colors"]["main"])
                    accent_color = random.choice(season_data["colors"]["accent"])
                    fabric = random.choice(season_data["fabrics"])
                    pattern = random.choice(season_data["patterns"])

                    # Format the outfit with selected colors and patterns
                    outfit = base_outfit.format(
                        color=main_color,
                        accent=accent_color,
                        fabric=fabric,
                        pattern=pattern,
                    )

                    # Create a detailed response
                    response = f"Untuk {season}, sebaiknya {outfit}. "
                    response += f"Warna yang trend di musim ini adalah {main_color} dan {accent_color}. "
                    response += f"Pilih bahan {fabric} yang cocok untuk musim ini."

                    # Determine label based on season
                    label_map = {"spring": 17, "summer": 15, "autumn": 18, "winter": 16}

                    dataset.append(
                        {
                            "query": query,
                            "response": response,
                            "label": label_map[season],
                            "gender": gender,
                            "skin_tone": "neutral",
                        }
                    )

                    # Add variations with skin tone for more diversity
                    if random.random() < 0.3:  # 30% chance to add skin tone variation
                        skin_tones = list(self.skin_tones.keys())
                        skin_tones.extend(list(self.extended_skin_tones.keys()))
                        skin_tone = random.choice(skin_tones)

                        if skin_tone in self.skin_tones:
                            skin_tone_term = random.choice(self.skin_tones[skin_tone])
                        else:
                            skin_tone_term = random.choice(
                                self.extended_skin_tones[skin_tone]
                            )

                        # Create a query with skin tone
                        query_with_skin = f"Outfit {season} untuk {gender_term} dengan kulit {skin_tone_term}?"

                        # Add color recommendation based on skin tone
                        if skin_tone in self.extended_color_recommendations:
                            best_colors = random.sample(
                                self.extended_color_recommendations[skin_tone]["best"],
                                2,
                            )
                            avoid_colors = random.sample(
                                self.extended_color_recommendations[skin_tone]["avoid"],
                                1,
                            )

                            color_advice = f" Untuk tone kulit {skin_tone_term}, warna {best_colors[0]} dan {best_colors[1]} "
                            color_advice += (
                                f"sangat flattering. Hindari warna {avoid_colors[0]}."
                            )

                            response_with_skin = response + color_advice
                        else:
                            response_with_skin = response

                        dataset.append(
                            {
                                "query": query_with_skin,
                                "response": response_with_skin,
                                "label": label_map[season],
                                "gender": gender,
                                "skin_tone": skin_tone,
                            }
                        )

        return pd.DataFrame(dataset)

    def generate_weather_dataset(self, samples_per_category: int = 100) -> pd.DataFrame:
        """Generate a dataset focused on weather-appropriate fashion recommendations"""
        dataset = []
        weather_types = ["hot", "cold", "rainy", "windy"]

        # Fixed weather queries that don't reference skin_tone parameter
        safe_weather_queries = [
            "Baju apa yang cocok untuk cuaca {weather}?",
            "Outfit untuk hari yang {weather}?",
            "Pakaian yang nyaman di cuaca {weather}?",
            "Rekomendasi pakaian untuk {gender} saat cuaca {weather}?",
            "Style yang sesuai untuk cuaca {weather}?",
            "Pakaian {gender} yang cocok untuk hari {weather}?",
            "Tips fashion untuk cuaca {weather}?",
            "Outfit yang trendy untuk cuaca {weather}?",
            "Baju yang sebaiknya dipakai saat cuaca {weather}?",
            "Apa yang sebaiknya dipakai saat cuaca sedang {weather}?",
            "Rekomendasi fashion untuk menghadapi cuaca {weather}?",
            "Cara berpakaian yang tepat saat cuaca {weather}?",
            "Apa yang sebaiknya saya pakai hari ini jika cuaca {weather}?",
            "Outfit yang comfortable untuk cuaca {weather}?",
        ]

        for weather in weather_types:
            for gender in ["pria", "wanita", "neutral"]:
                for _ in range(samples_per_category):
                    # Create weather-specific query
                    template = random.choice(safe_weather_queries)

                    # Handle gender neutral queries
                    if gender == "neutral":
                        template = template.replace("{gender}", "")
                        query = template.format(weather=weather)
                    else:
                        gender_term = random.choice(self.genders[gender])
                        query = template.format(weather=weather, gender=gender_term)

                    # Get weather data
                    weather_data = self.weather_modifiers[weather]

                    # Select random materials and styles
                    material = random.choice(weather_data["materials"])
                    style = random.choice(weather_data["styles"])

                    # Create a detailed response
                    response = f"Untuk cuaca {weather}, sebaiknya kenakan pakaian berbahan {material} "
                    response += f"dengan style {style}. "

                    # Add specific recommendations based on weather type
                    if weather == "hot":
                        response += "Pilih pakaian longgar dengan warna cerah yang tidak menyerap panas. "
                        response += (
                            "Pastikan pakaian menyerap keringat dan cepat kering."
                        )
                    elif weather == "cold":
                        response += "Gunakan teknik berlapis untuk menjaga kehangatan. "
                        response += "Lapisan terdalam sebaiknya berbahan yang menyerap keringat, lapisan tengah untuk insulasi, dan lapisan luar tahan angin/air."
                    elif weather == "rainy":
                        response += "Hindari bahan yang menyerap air seperti denim dan katun tebal. "
                        response += "Pilih sepatu anti air dan bawalah payung atau jas hujan lipat."
                    elif weather == "windy":
                        response += "Gunakan pakaian yang pas di badan agar tidak tertiup angin. "
                        response += "Pilih outer layer dengan closure yang kuat seperti zipper atau kancing."

                    # Determine label based on weather
                    label_map = {"hot": 11, "cold": 12, "rainy": 13, "windy": 14}

                    dataset.append(
                        {
                            "query": query,
                            "response": response,
                            "label": label_map[weather],
                            "gender": gender,
                            "skin_tone": "neutral",
                        }
                    )

                    # Add variations with skin tone for more diversity
                    if random.random() < 0.3:  # 30% chance to add skin tone variation
                        skin_tones = list(self.skin_tones.keys())
                        skin_tones.extend(list(self.extended_skin_tones.keys()))
                        skin_tone = random.choice(skin_tones)

                        if skin_tone in self.skin_tones:
                            skin_tone_term = random.choice(self.skin_tones[skin_tone])
                        else:
                            skin_tone_term = random.choice(
                                self.extended_skin_tones[skin_tone]
                            )

                        # Create a query with skin tone - manually constructed to avoid template issues
                        query_with_skin = f"Pakaian untuk cuaca {weather} untuk {gender_term} dengan kulit {skin_tone_term}?"

                        dataset.append(
                            {
                                "query": query_with_skin,
                                "response": response,
                                "label": label_map[weather],
                                "gender": gender,
                                "skin_tone": skin_tone,
                            }
                        )

        return pd.DataFrame(dataset)

    def generate_skin_tone_gender_dataset(self, samples_per_combination: int = 75):
        """Generate a dataset focused on skin tone and gender-specific fashion advice"""
        dataset = []

        # Query templates specifically for color advice
        color_query_templates = [
            "Warna apa yang cocok untuk {gender} dengan kulit {skin_tone}?",
            "Warna yang bagus untuk {gender} berkulit {skin_tone}?",
            "Saya {gender} dengan warna kulit {skin_tone}, warna apa yang flattering?",
            "Rekomendasi warna pakaian untuk {gender} dengan tone kulit {skin_tone}?",
            "Kombinasi warna untuk {gender} dengan kulit {skin_tone}?",
            "{gender} berkulit {skin_tone} sebaiknya mengenakan warna apa?",
            "Warna-warna apa yang membuat {gender} dengan kulit {skin_tone} terlihat lebih menarik?",
            "Pallete warna yang cocok untuk {gender} dengan tone kulit {skin_tone}?",
            "Warna busana yang membuat kulit {skin_tone} {gender} terlihat lebih bersinar?",
            "Sebagai {gender} dengan warna kulit {skin_tone}, warna apa yang sebaiknya saya pilih?",
            "Warna pakaian apa yang cocok dengan {gender} yang memiliki kulit {skin_tone}?",
            "Warna-warna yang menyanjung kulit {skin_tone} untuk {gender}?",
            "Warna apa yang harus dihindari oleh {gender} dengan kulit {skin_tone}?",
            "Warna yang paling sesuai dengan tone kulit {skin_tone} untuk {gender}?",
            "Sebagai {gender} berkulit {skin_tone}, warna apa yang paling cocok untuk formal?",
        ]

        # Generate specific queries for standard skin tones
        for skin_tone in ["light", "dark", "very_light", "medium", "very_dark"]:
            for gender in ["pria", "wanita"]:
                for _ in range(samples_per_combination):
                    # Create color-specific queries
                    template = random.choice(color_query_templates)

                    if skin_tone in self.skin_tones:
                        skin_tone_term = random.choice(self.skin_tones[skin_tone])
                    else:
                        skin_tone_term = random.choice(
                            self.extended_skin_tones[skin_tone]
                        )

                    gender_term = random.choice(self.genders[gender])

                    query = template.format(
                        gender=gender_term, skin_tone=skin_tone_term
                    )

                    # Create detailed color recommendations
                    if skin_tone in self.extended_color_recommendations:
                        best_colors = self.extended_color_recommendations[skin_tone][
                            "best"
                        ]
                        avoid_colors = self.extended_color_recommendations[skin_tone][
                            "avoid"
                        ]
                    else:
                        best_colors = self.color_palettes[
                            "light" if "light" in skin_tone else "dark"
                        ]["formal"]
                        avoid_colors = [
                            "warna yang terlalu kontras dengan kulit Anda",
                            "tone yang mirip dengan warna kulit Anda",
                        ]

                    response = f"Untuk {gender_term} dengan kulit {skin_tone_term}, "
                    response += f"warna yang sangat cocok adalah {', '.join(random.sample(best_colors, 3))}. "
                    response += f"Sebaiknya hindari {', '.join(random.sample(avoid_colors, 2))} "
                    response += f"karena kurang flattering untuk tone kulit Anda."

                    # Add formal/casual distinction randomly
                    if random.random() < 0.5:
                        formal_or_casual = random.choice(["formal", "casual"])
                        response += f" Untuk acara {formal_or_casual}, "

                        if formal_or_casual == "formal":
                            if skin_tone in ["light", "very_light"]:
                                colors = [
                                    "navy blue",
                                    "burgundy",
                                    "charcoal",
                                    "royal purple",
                                    "emerald",
                                ]
                            else:
                                colors = [
                                    "bright white",
                                    "cobalt blue",
                                    "royal purple",
                                    "ruby red",
                                    "emerald green",
                                ]
                        else:  # casual
                            if skin_tone in ["light", "very_light"]:
                                colors = [
                                    "pastel blue",
                                    "light pink",
                                    "mint green",
                                    "soft lavender",
                                    "powder blue",
                                ]
                            else:
                                colors = [
                                    "bright yellow",
                                    "electric blue",
                                    "coral",
                                    "turquoise",
                                    "hot pink",
                                ]

                        response += f"warna {', '.join(random.sample(colors, 2))} akan terlihat sangat bagus."

                    # Map to appropriate label
                    label_map = {
                        ("pria", "light"): 0,
                        ("pria", "very_light"): 0,
                        ("wanita", "light"): 1,
                        ("wanita", "very_light"): 1,
                        ("pria", "dark"): 2,
                        ("pria", "medium"): 2,
                        ("pria", "very_dark"): 2,
                        ("wanita", "dark"): 3,
                        ("wanita", "medium"): 3,
                        ("wanita", "very_dark"): 3,
                    }

                    label = label_map.get((gender, skin_tone), 19)

                    dataset.append(
                        {
                            "query": query,
                            "response": response,
                            "label": label,
                            "gender": gender,
                            "skin_tone": skin_tone,
                        }
                    )

                    # Add specific occasion recommendations
                    if random.random() < 0.3:  # 30% chance
                        occasions = [
                            "interview kerja",
                            "pesta",
                            "acara formal",
                            "kencan",
                            "hangout",
                            "wedding",
                            "business meeting",
                            "graduation",
                            "dinner",
                            "beach day",
                        ]
                        occasion = random.choice(occasions)

                        occasion_query = f"Outfit dan warna untuk {gender_term} berkulit {skin_tone_term} ke {occasion}?"

                        # Create specific outfit recommendation with color advice
                        if "formal" in occasion or occasion in [
                            "interview kerja",
                            "business meeting",
                            "graduation",
                        ]:
                            if gender == "pria":
                                outfit = random.choice(
                                    [
                                        "setelan jas dengan kemeja dan dasi",
                                        "blazer dengan kemeja dan celana bahan",
                                        "kemeja formal dengan celana wool",
                                    ]
                                )
                            else:
                                outfit = random.choice(
                                    [
                                        "blazer dengan rok pensil",
                                        "dress formal",
                                        "blus formal dengan celana bahan",
                                    ]
                                )
                        else:
                            if gender == "pria":
                                outfit = random.choice(
                                    [
                                        "kemeja casual dengan jeans",
                                        "polo shirt dengan chino",
                                        "t-shirt dengan celana pendek",
                                    ]
                                )
                            else:
                                outfit = random.choice(
                                    [
                                        "dress casual",
                                        "blus dengan rok A-line",
                                        "top dengan jeans high-waisted",
                                    ]
                                )

                        # Get appropriate colors
                        if skin_tone in self.extended_color_recommendations:
                            best_colors = random.sample(
                                self.extended_color_recommendations[skin_tone]["best"],
                                1,
                            )[0]
                        else:
                            best_colors = random.choice(
                                self.color_palettes[
                                    "light" if "light" in skin_tone else "dark"
                                ]["formal"]
                            )

                        occasion_response = f"Untuk {occasion}, {gender_term} berkulit {skin_tone_term} bisa mengenakan {outfit} "
                        occasion_response += f"dengan warna {best_colors} yang akan sangat menyanjung tone kulit Anda."

                        dataset.append(
                            {
                                "query": occasion_query,
                                "response": occasion_response,
                                "label": label,
                                "gender": gender,
                                "skin_tone": skin_tone,
                            }
                        )

        return pd.DataFrame(dataset)

    def generate_dataset(self, samples_per_category: int = 250) -> pd.DataFrame:
        """Generate a comprehensive dataset with all categories"""
        dataset = []

        for occasion_type, details in self.templates["occasions"].items():
            # Determine number of samples based on category type
            if details["gender"] == "neutral" and details["skin_tone"] == "neutral":
                current_samples = (
                    samples_per_category * 2
                )  # Double the samples for neutral categories
            else:
                current_samples = samples_per_category

            for _ in range(current_samples):
                event = random.choice(details["events"])

                # For neutral categories (weather, general events)
                if details["gender"] == "neutral" and details["skin_tone"] == "neutral":
                    # Generate multiple variations for neutral categories
                    templates = [
                        f"Apa yang cocok untuk {event}?",
                        f"Rekomendasi pakaian untuk {event}?",
                        f"Bagaimana cara berpakaian untuk {event}?",
                        f"Outfit yang bagus untuk {event}?",
                        f"Mau ke {event}, sebaiknya pakai apa ya?",
                        f"Style yang sesuai untuk {event}?",
                        f"Fashion tips untuk {event}?",
                        f"Pakaian yang nyaman untuk {event}?",
                        f"Panduan berpakaian untuk {event}?",
                        f"Referensi outfit untuk {event}?",
                    ]
                    query = random.choice(templates)
                else:
                    template = random.choice(self.templates["query_templates"])
                    query = self.generate_variation(
                        template, event, details["gender"], details["skin_tone"]
                    )

                response = random.choice(details["responses"])
                if details["skin_tone"] in ["light", "dark"]:
                    color_rec = self.generate_color_recommendation(
                        details["skin_tone"], occasion_type
                    )
                    response = response + color_rec

                dataset.append(
                    {
                        "query": query,
                        "response": response,
                        "label": details["label"],
                        "gender": details["gender"],
                        "skin_tone": details["skin_tone"],
                    }
                )

                # Add variations with higher probability for neutral categories
                variation_prob = 0.6 if details["gender"] == "neutral" else 0.3
                if random.random() < variation_prob:
                    if details["gender"] == "neutral":
                        variant_template = random.choice(templates)
                    else:
                        variant_template = random.choice(
                            self.templates["query_templates"]
                        )
                        variant_template = self.generate_variation(
                            variant_template,
                            event,
                            details["gender"],
                            details["skin_tone"],
                        )

                    dataset.append(
                        {
                            "query": variant_template,
                            "response": response,
                            "label": details["label"],
                            "gender": details["gender"],
                            "skin_tone": details["skin_tone"],
                        }
                    )

        return pd.DataFrame(dataset)


def generate_enhanced_dataset():
    """Generate an enhanced dataset with all categories and save it"""
    # Create the generator
    generator = EnhancedFashionDatasetGenerator()

    # Generate datasets for each category
    general_df = generator.generate_dataset(samples_per_category=200)
    print(f"General dataset size: {len(general_df)}")

    seasonal_df = generator.generate_seasonal_dataset(samples_per_category=100)
    print(f"Seasonal dataset size: {len(seasonal_df)}")

    weather_df = generator.generate_weather_dataset(samples_per_category=100)
    print(f"Weather dataset size: {len(weather_df)}")

    skin_tone_df = generator.generate_skin_tone_gender_dataset(
        samples_per_combination=75
    )
    print(f"Skin tone specific dataset size: {len(skin_tone_df)}")

    # Combine all datasets
    combined_df = pd.concat(
        [general_df, seasonal_df, weather_df, skin_tone_df], ignore_index=True
    )

    # Remove duplicates
    combined_df = combined_df.drop_duplicates(subset=["query"])
    print(f"Combined dataset size after removing duplicates: {len(combined_df)}")

    # Save combined dataset
    os.makedirs("data/processed", exist_ok=True)
    combined_df.to_csv("data/processed/enhanced_dataset.csv", index=False)
    print("Enhanced dataset saved to data/processed/enhanced_dataset.csv")

    # Print distribution
    print("\nLabel distribution in enhanced dataset:")
    label_counts = combined_df["label"].value_counts().sort_index()
    for label, count in label_counts.items():
        print(f"Label {label}: {count} examples")

    print("\nGender distribution:")
    gender_counts = combined_df["gender"].value_counts()
    for gender, count in gender_counts.items():
        print(f"{gender}: {count} examples")

    print("\nSkin tone distribution:")
    skin_tone_counts = combined_df["skin_tone"].value_counts()
    for tone, count in skin_tone_counts.items():
        print(f"{tone}: {count} examples")

    return combined_df


def combine_with_original_dataset(enhanced_df=None):
    """Combine the enhanced dataset with the original dataset"""
    # Load original dataset
    original_df = pd.read_csv("train/dataset.csv")
    print(f"Original dataset size: {len(original_df)}")

    # Add gender and skin_tone columns to original dataset if they don't exist
    if "gender" not in original_df.columns:
        original_df["gender"] = "neutral"
    if "skin_tone" not in original_df.columns:
        original_df["skin_tone"] = "neutral"

    # Generate enhanced dataset if not provided
    if enhanced_df is None:
        generator = EnhancedFashionDatasetGenerator()
        enhanced_df = generator.generate_dataset(samples_per_category=150)

        # Generate specific skin tone and gender data
        seasonal_df = generator.generate_seasonal_dataset(samples_per_category=75)
        weather_df = generator.generate_weather_dataset(samples_per_category=75)
        skin_tone_df = generator.generate_skin_tone_gender_dataset(
            samples_per_combination=50
        )

        # Combine all enhanced datasets
        enhanced_df = pd.concat(
            [enhanced_df, seasonal_df, weather_df, skin_tone_df], ignore_index=True
        )
        enhanced_df = enhanced_df.drop_duplicates(subset=["query"])

    print(f"Enhanced dataset size: {len(enhanced_df)}")

    # Combine datasets
    combined_df = pd.concat([original_df, enhanced_df], ignore_index=True)

    # Remove duplicates
    combined_df = combined_df.drop_duplicates(subset=["query"])
    print(f"Combined dataset size after removing duplicates: {len(combined_df)}")

    # Save combined dataset
    os.makedirs("data/processed", exist_ok=True)
    combined_df.to_csv("data/processed/combined_enhanced_dataset.csv", index=False)
    print("Combined dataset saved to data/processed/combined_enhanced_dataset.csv")

    # Print distribution
    print("\nLabel distribution in combined dataset:")
    label_counts = combined_df["label"].value_counts().sort_index()
    for label, count in label_counts.items():
        print(f"Label {label}: {count} examples")

    print("\nGender distribution:")
    gender_counts = combined_df["gender"].value_counts()
    for gender, count in gender_counts.items():
        print(f"{gender}: {count} examples")

    print("\nSkin tone distribution:")
    skin_tone_counts = combined_df["skin_tone"].value_counts()
    for tone, count in skin_tone_counts.items():
        print(f"{tone}: {count} examples")


if __name__ == "__main__":
    # Generate enhanced dataset
    enhanced_df = generate_enhanced_dataset()

    # Combine with original dataset
    combine_with_original_dataset(enhanced_df)
