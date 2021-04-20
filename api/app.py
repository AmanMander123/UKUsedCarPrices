import pandas as pd
from flask import Flask, request, render_template, jsonify
import pickle

MODEL_PATH = 'lin_reg_model.pkl'

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def predict():
    try:
        model = pickle.load(open(MODEL_PATH, "rb"))
        features_str = 'year mileage tax mpg engineSize	model_1Series	model_2Series	model_3Series	model_4Series	model_5Series	model_6Series	model_7Series	model_8Series	model_AClass	model_A1	model_A2	model_A3	model_A4	model_A5	model_A6	model_A7	model_A8	model_Accent	model_Adam	model_Agila	model_Amarok	model_Amica	model_Ampera	model_Antara	model_Arteon	model_Astra	model_Auris	model_Avensis	model_Aygo	model_BClass	model_B_MAX	model_Beetle	model_CClass	model_C_HR	model_C_MAX	model_CC	model_CLClass	model_CLAClass	model_CLCClass	model_CLK	model_CLSClass	model_Caddy	model_CaddyLife	model_CaddyMaxi	model_CaddyMaxiLife	model_California	model_Camry	model_Caravelle	model_Cascada	model_Citigo	model_ComboLife	model_Corolla	model_Corsa	model_CrosslandX	model_EClass	model_EcoSport	model_Edge	model_Eos	model_Escort	model_Fabia	model_Fiesta	model_Focus	model_Fox	model_Fusion	model_GClass	model_GLClass	model_GLAClass	model_GLBClass	model_GLCClass	model_GLEClass	model_GLSClass	model_GT86	model_GTC	model_Galaxy	model_Getz	model_Golf	model_GolfSV	model_GrandC_MAX	model_GrandTourneoConnect	model_GrandlandX	model_Hilux	model_I10	model_I20	model_I30	model_I40	model_I800	model_IQ	model_IX20	model_IX35	model_Insignia	model_Ioniq	model_Jetta	model_KA	model_Ka_plus	model_Kadjar	model_Kamiq	model_Karoq	model_Kodiaq	model_Kona	model_Kuga	model_LandCruiser	model_MClass	model_M2	model_M3	model_M4	model_M5	model_M6	model_Meriva	model_Mokka	model_MokkaX	model_Mondeo	model_Mustang	model_Octavia	model_PROACEVERSO	model_Passat	model_Polo	model_Prius	model_Puma	model_Q2	model_Q3	model_Q5	model_Q7	model_Q8	model_RClass	model_R8	model_RAV4	model_RS3	model_RS4	model_RS5	model_RS6	model_RS7	model_Ranger	model_Rapid	model_Roomster	model_SClass	model_S_MAX	model_S3	model_S4	model_S5	model_S8	model_SLCLASS	model_SLK	model_SQ5	model_SQ7	model_SantaFe	model_Scala	model_Scirocco	model_Sharan	model_Shuttle	model_Streetka	model_Superb	model_Supra	model_T_Cross	model_T_Roc	model_TT	model_Terracan	model_Tigra	model_Tiguan	model_TiguanAllspace	model_Touareg	model_Touran	model_TourneoConnect	model_TourneoCustom	model_TransitTourneo	model_Tucson	model_Up	model_UrbanCruiser	model_VClass	model_Vectra	model_Veloster	model_Verso	model_Verso_S	model_Viva	model_Vivaro	model_X_CLASS	model_X1	model_X2	model_X3	model_X4	model_X5	model_X6	model_X7	model_Yaris	model_Yeti	model_YetiOutdoor	model_Z3	model_Z4	model_Zafira	model_ZafiraTourer	model_i3	model_i8	model_180	model_200	model_220	model_230	transmission_Automatic	transmission_Manual	transmission_Other	transmission_Semi_Auto	fuelType_Diesel	fuelType_Electric	fuelType_Hybrid	fuelType_Other	fuelType_Petrol	make_Audi	make_BMW	make_C_Class	make_Focus	make_Ford	make_Hyundai	make_Mercedes	make_Skoda	make_Toyota	make_VW	make_Vauxhall'
        feature_dict = {}
        splits = features_str.split()
        for item in splits:
            feature_dict[item] = [0]

        # Define feature vector

        # Process numerical features
        feature_dict['year'] = [int(request.args['year'])]
        feature_dict['mileage'] = [int(request.args['mileage'])]
        feature_dict['tax'] = [int(request.args['tax'])]
        feature_dict['mpg'] = [int(request.args['mpg'])]
        feature_dict['engineSize'] = [float(str(request.args['enginesize']))]

        # Process categorical variables
        make = str(request.args['make'])
        make_var = 'make_' + make
        feature_dict[make_var] = [1]

        transmission = str(request.args['transmission'])
        transmission_var = 'transmission_' + transmission
        feature_dict[transmission_var] = [1]

        fueltype = str(request.args['fueltype'])
        fueltype_var = 'fuelType_' + fueltype
        feature_dict[fueltype_var] = [1]

        veh_model = str(request.args['model'])
        veh_model_var = 'model_' + veh_model
        feature_dict[veh_model_var] = [1]

        df_prod = pd.DataFrame.from_dict(feature_dict)

        result = {
            'result': str(model.predict(df_prod)[0])
        }
    except:
        result = {
            'result': 'Please enter valid input parameters'
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run()
