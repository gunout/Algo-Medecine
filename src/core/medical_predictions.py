import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import hashlib

class EtatSante(Enum):
    CRITIQUE = (0.1, "CRITIQUE")
    GRAVE = (0.3, "GRAVE")
    MODERE = (0.6, "MODÉRÉ")
    STABLE = (0.8, "STABLE")
    EXCELLENT = (0.95, "EXCELLENT")
    
    def __init__(self, score: float, label: str):
        self.score = score
        self.label = label

class AlgoVeriteMedical:
    """
    Système de recherche sanitaire et prédiction de rétablissement
    basé sur l'analyse pyramidale et l'harmonie biomathématique
    """
    
    def __init__(self):
        self.base_connaissances_medicales = self._initialiser_base_medicale()
        self.historique_patients = {}
        self.protocoles_traitements = self._initialiser_protocoles()
        self.modeles_prediction = self._initialiser_modeles_prediction()
        
    def _initialiser_base_medicale(self) -> Dict:
        """Initialise la base de connaissances médicales"""
        return {
            'pathologies_reference': {
                'GRIPPE': {
                    'severite_base': 0.4, 
                    'duree_moyenne': 7, 
                    'resilience': 0.8,
                    'symptomes_typiques': ['FIÈVRE', 'TOUX', 'FATIGUE', 'DOULEURS_MUSCULAIRES']
                },
                'COVID': {
                    'severite_base': 0.7, 
                    'duree_moyenne': 14, 
                    'resilience': 0.6,
                    'symptomes_typiques': ['FIÈVRE', 'TOUX', 'DYSPNÉE', 'ANOSMIE', 'FATIGUE']
                },
                'BRONCHITE': {
                    'severite_base': 0.5, 
                    'duree_moyenne': 10, 
                    'resilience': 0.7,
                    'symptomes_typiques': ['TOUX', 'EXPECTORATION', 'DYSPNÉE']
                },
                'PNEUMONIE': {
                    'severite_base': 0.8, 
                    'duree_moyenne': 21, 
                    'resilience': 0.5,
                    'symptomes_typiques': ['FIÈVRE_ÉLEVÉE', 'TOUX_GRASSE', 'DOULEUR_THORACIQUE', 'DYSPNÉE']
                },
                'MIGRAINE': {
                    'severite_base': 0.3, 
                    'duree_moyenne': 2, 
                    'resilience': 0.9,
                    'symptomes_typiques': ['CEPHALÉE', 'PHOTOPHOBIE', 'NAUSÉE']
                }
            },
            'traitements_reference': {
                'ANTIVIRAL': {
                    'efficacite': 0.7, 
                    'delai_action': 2, 
                    'compatibilite': 0.8,
                    'pathologies': ['GRIPPE', 'COVID']
                },
                'ANTIBIOTIQUE': {
                    'efficacite': 0.8, 
                    'delai_action': 3, 
                    'compatibilite': 0.7,
                    'pathologies': ['BRONCHITE', 'PNEUMONIE']
                },
                'ANTIINFLAMMATOIRE': {
                    'efficacite': 0.6, 
                    'delai_action': 1, 
                    'compatibilite': 0.9,
                    'pathologies': ['GRIPPE', 'COVID', 'BRONCHITE', 'PNEUMONIE']
                },
                'IMMUNOSTIMULANT': {
                    'efficacite': 0.5, 
                    'delai_action': 5, 
                    'compatibilite': 0.95,
                    'pathologies': ['GRIPPE', 'COVID']
                },
                'ANALGESIQUE': {
                    'efficacite': 0.4, 
                    'delai_action': 1, 
                    'compatibilite': 0.85,
                    'pathologies': ['MIGRAINE', 'GRIPPE']
                },
                'BRONCHODILATATEUR': {
                    'efficacite': 0.7, 
                    'delai_action': 2, 
                    'compatibilite': 0.8,
                    'pathologies': ['BRONCHITE', 'PNEUMONIE']
                }
            },
            'profils_patients': {
                'JEUNE': {
                    'resilience': 0.9, 
                    'reponse_traitement': 0.8, 
                    'recuperation': 0.85,
                    'age_min': 0, 'age_max': 25
                },
                'ADULTE': {
                    'resilience': 0.7, 
                    'reponse_traitement': 0.7, 
                    'recuperation': 0.7,
                    'age_min': 26, 'age_max': 60
                },
                'SENIOR': {
                    'resilience': 0.5, 
                    'reponse_traitement': 0.6, 
                    'recuperation': 0.5,
                    'age_min': 61, 'age_max': 120
                },
                'IMMUNODEPRIME': {
                    'resilience': 0.3, 
                    'reponse_traitement': 0.4, 
                    'recuperation': 0.3,
                    'age_min': 0, 'age_max': 120
                }
            }
        }
    
    def _initialiser_protocoles(self) -> Dict:
        """Initialise les protocoles de traitement optimisés"""
        return {
            'PROTOCOLE_STANDARD_GRIPPE': {
                'pathologies': ['GRIPPE'],
                'traitements': ['ANTIVIRAL', 'ANTIINFLAMMATOIRE'],
                'duree_moyenne': 7,
                'efficacite_attendue': 0.75,
                'conditions': ['FIÈVRE < 39°C', 'AUCUNE_DETRESSE_RESPIRATOIRE']
            },
            'PROTOCOLE_INTENSIF_COVID': {
                'pathologies': ['COVID'],
                'traitements': ['ANTIVIRAL', 'ANTIINFLAMMATOIRE', 'IMMUNOSTIMULANT'],
                'duree_moyenne': 14,
                'efficacite_attendue': 0.65,
                'conditions': ['TOUS_LES_CAS_CONFIRMÉS']
            },
            'PROTOCOLE_BRONCHITE': {
                'pathologies': ['BRONCHITE'],
                'traitements': ['ANTIBIOTIQUE', 'BRONCHODILATATEUR'],
                'duree_moyenne': 10,
                'efficacite_attendue': 0.80,
                'conditions': ['EXPECTORATION_PURULENTE']
            },
            'PROTOCOLE_PNEUMONIE': {
                'pathologies': ['PNEUMONIE'],
                'traitements': ['ANTIBIOTIQUE', 'ANTIINFLAMMATOIRE', 'BRONCHODILATATEUR'],
                'duree_moyenne': 21,
                'efficacite_attendue': 0.70,
                'conditions': ['CONFIRMATION_RADIOGRAPHIQUE']
            },
            'PROTOCOLE_MIGRAINE': {
                'pathologies': ['MIGRAINE'],
                'traitements': ['ANALGESIQUE'],
                'duree_moyenne': 2,
                'efficacite_attendue': 0.85,
                'conditions': ['CEPHALÉE_SANS_COMPLICATIONS']
            }
        }
    
    def _initialiser_modeles_prediction(self) -> Dict:
        """Initialise les modèles de prédiction de rétablissement"""
        return {
            'modele_linearite': 0.25,
            'modele_harmonie': 0.35,
            'modele_resonance': 0.20,
            'modele_adaptation': 0.20
        }
    
    def analyser_patient(self, patient_data: Dict) -> Dict:
        """
        Analyse complète d'un patient et prédiction de son rétablissement
        """
        # Validation des données
        self._valider_donnees_patient(patient_data)
        
        # Analyse pyramidale de la condition du patient
        analyse_sante = self._analyser_condition_patient(patient_data)
        
        # Recherche de traitement optimal
        traitements_recommandes = self._rechercher_traitements_optimaux(patient_data, analyse_sante)
        
        # Prédiction de rétablissement
        prediction = self._predire_retablissement(patient_data, analyse_sante, traitements_recommandes)
        
        # Génération du plan de soins
        plan_soins = self._generer_plan_soins(prediction, traitements_recommandes, patient_data)
        
        # Calcul du score de confiance global
        score_confiance = self._calculer_confiance_globale(analyse_sante, prediction, traitements_recommandes)
        
        resultat = {
            'patient_id': patient_data.get('id', self._generer_id_patient(patient_data)),
            'timestamp_analyse': datetime.now().isoformat(),
            'condition_actuelle': analyse_sante,
            'traitements_recommandes': traitements_recommandes,
            'prediction_retablissement': prediction,
            'plan_soins_personnalise': plan_soins,
            'facteurs_pronostiques': self._identifier_facteurs_pronostiques(analyse_sante, patient_data),
            'recommandations_suivi': self._generer_recommandations_suivi(prediction, patient_data),
            'score_confiance_global': score_confiance,
            'avertissements': self._generer_avertissements(analyse_sante, prediction)
        }
        
        # Archivage
        self.historique_patients[resultat['patient_id']] = resultat
        
        return resultat
    
    def _valider_donnees_patient(self, patient_data: Dict):
        """Valide les données du patient"""
        requis = ['pathologie', 'symptomes', 'profil']
        for champ in requis:
            if champ not in patient_data:
                raise ValueError(f"Champ requis manquant: {champ}")
        
        if patient_data['pathologie'].upper() not in self.base_connaissances_medicales['pathologies_reference']:
            raise ValueError(f"Pathologie non reconnue: {patient_data['pathologie']}")
    
    def _generer_id_patient(self, patient_data: Dict) -> str:
        """Génère un ID unique pour le patient"""
        data_string = f"{patient_data.get('pathologie', '')}{patient_data.get('profil', {})}"
        return f"PAT_{hashlib.sha256(data_string.encode()).hexdigest()[:8]}"
    
    def _analyser_condition_patient(self, patient_data: Dict) -> Dict:
        """Analyse la condition médicale du patient via l'algorithme pyramidal"""
        
        # Conversion des données en séquences numériques
        symptomes_codes = self._coder_symptomes(patient_data.get('symptomes', []))
        pathologie_codes = self._coder_pathologie(patient_data.get('pathologie', ''))
        profil_codes = self._coder_profil_patient(patient_data.get('profil', {}))
        
        # Construction de la pyramide de santé
        pyramide_sante = self._construire_pyramide_sante(symptomes_codes, pathologie_codes, profil_codes)
        
        return {
            'pyramide_sante': pyramide_sante,
            'score_gravite': self._calculer_gravite(symptomes_codes, pathologie_codes, patient_data),
            'potentiel_retablissement': self._evaluer_potentiel_retablissement(pyramide_sante),
            'resilience_patient': self._calculer_resilience(profil_codes, pyramide_sante, patient_data),
            'harmonie_biologique': self._evaluer_harmonie_biologique(pyramide_sante),
            'etat_sante': self._determiner_etat_sante(pyramide_sante, patient_data),
            'facteurs_aggravants': self._identifier_facteurs_aggravants(patient_data),
            'indicateurs_favorables': self._identifier_indicateurs_favorables(pyramide_sante)
        }
    
    def _coder_symptomes(self, symptomes: List[str]) -> List[int]:
        """Code les symptômes en séquence numérique"""
        if not symptomes:
            return [0]
        
        codes = []
        for symptome in symptomes:
            # Conversion du symptôme en code numérique basé sur sa gravité présumée
            gravite_symptome = self._estimer_gravite_symptome(symptome)
            code = int(gravite_symptome * 100)
            codes.append(code)
        
        return codes if codes else [0]
    
    def _estimer_gravite_symptome(self, symptome: str) -> float:
        """Estime la gravité d'un symptôme"""
        gravites = {
            'FIÈVRE_LEGERE': 0.3, 'FIÈVRE': 0.5, 'FIÈVRE_ÉLEVÉE': 0.8,
            'TOUX': 0.3, 'TOUX_GRASSE': 0.4, 'TOUX_SÈCHE': 0.3,
            'DYSPNÉE': 0.7, 'DYSPNÉE_SEVERE': 0.9,
            'DOULEURS_MUSCULAIRES': 0.3, 'CEPHALÉE': 0.4,
            'FATIGUE': 0.3, 'ANOSMIE': 0.2, 'NAUSÉE': 0.4
        }
        
        return gravites.get(symptome.upper(), 0.3)
    
    def _coder_pathologie(self, pathologie: str) -> List[int]:
        """Code la pathologie en séquence numérique"""
        patho_ref = self.base_connaissances_medicales['pathologies_reference'].get(
            pathologie.upper(), 
            {'severite_base': 0.5, 'duree_moyenne': 10, 'resilience': 0.5}
        )
        
        return [
            int(patho_ref['severite_base'] * 100),
            patho_ref['duree_moyenne'],
            int(patho_ref['resilience'] * 100)
        ]
    
    def _coder_profil_patient(self, profil: Dict) -> List[int]:
        """Code le profil patient en séquence numérique"""
        age_group = self._determiner_groupe_age(profil.get('age', 40))
        comorbidities = profil.get('comorbidities', 0)
        immunity_level = profil.get('immunity_level', 0.7)
        
        profil_ref = self.base_connaissances_medicales['profils_patients'].get(
            age_group,
            {'resilience': 0.7, 'reponse_traitement': 0.7, 'recuperation': 0.7}
        )
        
        return [
            int(profil_ref['resilience'] * 100),
            int(profil_ref['reponse_traitement'] * 100),
            int(immunity_level * 100),
            min(comorbidities * 20, 100)  # Limiter l'impact des comorbidités
        ]
    
    def _determiner_groupe_age(self, age: int) -> str:
        """Détermine le groupe d'âge du patient"""
        if age <= 25:
            return 'JEUNE'
        elif age <= 60:
            return 'ADULTE'
        else:
            return 'SENIOR'
    
    def _construire_pyramide_sante(self, symptomes: List[int], pathologie: List[int], profil: List[int]) -> Dict:
        """Construit la pyramide de santé du patient"""
        
        # Base: combinaison pondérée des trois dimensions
        base = symptomes + pathologie + profil
        
        pyramide = {
            'base': base,
            'superieure': [],
            'inferieure': []
        }
        
        # Construction partie supérieure (indicateurs d'amélioration)
        current = base.copy()
        while len(current) > 1:
            next_level = [current[i] + current[i+1] for i in range(len(current)-1)]
            pyramide['superieure'].insert(0, next_level)
            current = next_level
        
        # Construction partie inférieure (indicateurs de risque)
        current = base.copy()
        while len(current) > 1:
            next_level = [abs(current[i] - current[i+1]) for i in range(len(current)-1)]
            pyramide['inferieure'].append(next_level)
            current = next_level
        
        return pyramide
    
    def _calculer_gravite(self, symptomes: List[int], pathologie: List[int], patient_data: Dict) -> float:
        """Calcule le score de gravité de la condition"""
        if not symptomes or not pathologie:
            return 0.5
        
        # Gravité basée sur les symptômes
        severite_symptomes = sum(symptomes) / (len(symptomes) * 100) if symptomes else 0
        
        # Gravité basée sur la pathologie
        severite_pathologie = pathologie[0] / 100 if pathologie else 0.5
        
        # Facteur de comorbidités
        comorbidities_factor = min(patient_data.get('profil', {}).get('comorbidities', 0) * 0.1, 0.3)
        
        score_base = (severite_symptomes + severite_pathologie) / 2
        score_final = min(score_base + comorbidities_factor, 1.0)
        
        return max(0, score_final)
    
    def _evaluer_potentiel_retablissement(self, pyramide: Dict) -> float:
        """Évalue le potentiel de rétablissement du patient"""
        if not pyramide['superieure'] or not pyramide['inferieure']:
            return 0.5
        
        # Ratio d'harmonie entre amélioration et risques
        sommet = pyramide['superieure'][0][0] if pyramide['superieure'] else 0
        base_risque = pyramide['inferieure'][-1][0] if pyramide['inferieure'] else 1
        
        if base_risque == 0:
            base_risque = 1
        
        harmonie = 1.0 - min(abs(sommet - base_risque) / max(sommet, base_risque), 1)
        
        # Facteur de stabilité structurelle
        stabilite = 1.0 - (len(pyramide['inferieure']) / (len(pyramide['base']) * 2))
        
        return max(0, min((harmonie + stabilite) / 2, 1))
    
    def _calculer_resilience(self, profil: List[int], pyramide: Dict, patient_data: Dict) -> float:
        """Calcule la résilience du patient"""
        resilience_base = profil[0] / 100 if profil else 0.5
        
        # Facteur structurel de la pyramide
        symetrie = 1.0 - (abs(len(pyramide['superieure']) - len(pyramide['inferieure'])) / 
                          max(len(pyramide['superieure']), len(pyramide['inferieure']), 1))
        
        # Facteur d'immunité
        immunite = patient_data.get('profil', {}).get('immunity_level', 0.7)
        
        resilience_calculée = (resilience_base * 0.4 + symetrie * 0.3 + immunite * 0.3)
        
        return max(0, min(resilience_calculée, 1))
    
    def _evaluer_harmonie_biologique(self, pyramide: Dict) -> float:
        """Évalue l'harmonie biologique du patient"""
        if not pyramide['superieure'] or not pyramide['inferieure']:
            return 0.5
        
        # Équilibre entre les systèmes
        valeurs_sup = [item for niveau in pyramide['superieure'] for item in niveau]
        valeurs_inf = [item for niveau in pyramide['inferieure'] for item in niveau]
        
        if not valeurs_sup or not valeurs_inf:
            return 0.5
        
        moyenne_sup = np.mean(valeurs_sup)
        moyenne_inf = np.mean(valeurs_inf)
        
        if moyenne_sup == 0 or moyenne_inf == 0:
            return 0.5
        
        harmonie = 1.0 - abs(moyenne_sup - moyenne_inf) / max(moyenne_sup, moyenne_inf)
        return max(0, min(harmonie, 1))
    
    def _determiner_etat_sante(self, pyramide: Dict, patient_data: Dict) -> EtatSante:
        """Détermine l'état de santé global du patient"""
        score_gravite = self._calculer_gravite(
            self._coder_symptomes(patient_data.get('symptomes', [])),
            self._coder_pathologie(patient_data.get('pathologie', '')),
            patient_data
        )
        
        # Ajustement basé sur la résilience
        resilience = self._calculer_resilience(
            self._coder_profil_patient(patient_data.get('profil', {})),
            pyramide,
            patient_data
        )
        
        score_ajuste = score_gravite * (1 - resilience * 0.3)
        
        if score_ajuste >= 0.8:
            return EtatSante.CRITIQUE
        elif score_ajuste >= 0.6:
            return EtatSante.GRAVE
        elif score_ajuste >= 0.4:
            return EtatSante.MODERE
        elif score_ajuste >= 0.2:
            return EtatSante.STABLE
        else:
            return EtatSante.EXCELLENT
    
    def _identifier_facteurs_aggravants(self, patient_data: Dict) -> List[str]:
        """Identifie les facteurs aggravants"""
        facteurs = []
        profil = patient_data.get('profil', {})
        
        if profil.get('comorbidities', 0) >= 3:
            facteurs.append("Multiples comorbidités")
        
        if profil.get('age', 40) >= 65:
            facteurs.append("Âge avancé")
        
        if profil.get('immunity_level', 0.7) <= 0.4:
            facteurs.append("Immunodépression")
        
        symptomes = patient_data.get('symptomes', [])
        if 'DYSPNÉE_SEVERE' in symptomes:
            facteurs.append("Détresse respiratoire sévère")
        if 'FIÈVRE_ÉLEVÉE' in symptomes:
            facteurs.append("Fièvre élevée persistante")
        
        return facteurs
    
    def _identifier_indicateurs_favorables(self, pyramide: Dict) -> List[str]:
        """Identifie les indicateurs favorables"""
        indicateurs = []
        
        if self._evaluer_harmonie_biologique(pyramide) > 0.8:
            indicateurs.append("Harmonie biologique élevée")
        
        if self._evaluer_potentiel_retablissement(pyramide) > 0.7:
            indicateurs.append("Potentiel de rétablissement élevé")
        
        if len(pyramide['inferieure']) <= 3:
            indicateurs.append("Convergence rapide vers la stabilité")
        
        return indicateurs
    
    def _rechercher_traitements_optimaux(self, patient_data: Dict, analyse_sante: Dict) -> List[Dict]:
        """Recherche les traitements optimaux pour le patient"""
        pathologie = patient_data.get('pathologie', '').upper()
        profil = patient_data.get('profil', {})
        symptomes = patient_data.get('symptomes', [])
        
        traitements_candidats = []
        
        # Recherche dans les protocoles établis
        for protocole_nom, protocole in self.protocoles_traitements.items():
            if pathologie in protocole['pathologies']:
                for traitement_nom in protocole['traitements']:
                    traitement_ref = self.base_connaissances_medicales['traitements_reference'].get(
                        traitement_nom,
                        {'efficacite': 0.5, 'delai_action': 5, 'compatibilite': 0.5}
                    )
                    
                    # Calcul du score de compatibilité personnalisé
                    score_compatibilite = self._calculer_compatibilite_traitement(
                        traitement_ref, profil, analyse_sante, symptomes
                    )
                    
                    # Score global pondéré
                    score_global = (
                        traitement_ref['efficacite'] * 0.4 +
                        score_compatibilite * 0.4 +
                        (1 - traitement_ref['delai_action'] / 10) * 0.2  # Préférer les traitements rapides
                    )
                    
                    traitements_candidats.append({
                        'nom': traitement_nom,
                        'protocole': protocole_nom,
                        'efficacite_base': traitement_ref['efficacite'],
                        'compatibilite_personnalisee': score_compatibilite,
                        'score_global': score_global,
                        'delai_action_attendu': traitement_ref['delai_action'],
                        'indications': self._generer_indications_traitement(traitement_nom, symptomes)
                    })
        
        # Tri par score global décroissant
        traitements_candidats.sort(key=lambda x: x['score_global'], reverse=True)
        
        return traitements_candidats[:3]  # Retourne les 3 meilleurs traitements
    
    def _calculer_compatibilite_traitement(self, traitement: Dict, profil: Dict, analyse_sante: Dict, symptomes: List[str]) -> float:
        """Calcule la compatibilité personnalisée du traitement"""
        age_group = self._determiner_groupe_age(profil.get('age', 40))
        profil_ref = self.base_connaissances_medicales['profils_patients'].get(
            age_group,
            {'resilience': 0.7, 'reponse_traitement': 0.7, 'recuperation': 0.7}
        )
        
        # Facteurs de compatibilité
        facteurs = []
        
        # Réponse au traitement selon le profil
        facteurs.append(profil_ref['reponse_traitement'])
        
        # Harmonnie avec l'état du patient
        facteurs.append(analyse_sante['harmonie_biologique'])
        
        # Compatibilité avec la résilience
        resilience_ratio = min(analyse_sante['resilience_patient'] / traitement.get('compatibilite', 0.5), 1)
        facteurs.append(resilience_ratio)
        
        # Adéquation avec les symptômes
        adequation_symptomes = self._evaluer_adequation_symptomes(traitement, symptomes)
        facteurs.append(adequation_symptomes)
        
        return sum(facteurs) / len(facteurs)
    
    def _evaluer_adequation_symptomes(self, traitement: Dict, symptomes: List[str]) -> float:
        """Évalue l'adéquation du traitement avec les symptômes présents"""
        # Mapping simplifié des traitements et des symptômes qu'ils ciblent
        cibles_traitement = {
            'ANTIVIRAL': ['FIÈVRE', 'FATIGUE'],
            'ANTIBIOTIQUE': ['FIÈVRE_ÉLEVÉE', 'EXPECTORATION_PURULENTE'],
            'ANTIINFLAMMATOIRE': ['DOULEURS_MUSCULAIRES', 'CEPHALÉE', 'FIÈVRE'],
            'IMMUNOSTIMULANT': ['FATIGUE'],
            'ANALGESIQUE': ['CEPHALÉE', 'DOULEURS_MUSCULAIRES'],
            'BRONCHODILATATEUR': ['DYSPNÉE', 'TOUX']
        }
        
        symptomes_cibles = cibles_traitement.get(traitement['nom'], [])
        if not symptomes_cibles:
            return 0.5
        
        correspondances = sum(1 for symptome in symptomes if symptome in symptomes_cibles)
        return min(correspondances / len(symptomes_cibles), 1.0) if symptomes_cibles else 0.5
    
    def _generer_indications_traitement(self, traitement: str, symptomes: List[str]) -> List[str]:
        """Génère les indications spécifiques du traitement"""
        indications = {
            'ANTIVIRAL': ["Début précoce de la maladie", "Symptômes viraux typiques"],
            'ANTIBIOTIQUE': ["Suspicion d'infection bactérienne", "Expectoration purulente"],
            'ANTIINFLAMMATOIRE': ["Inflammation importante", "Douleurs musculaires"],
            'IMMUNOSTIMULANT': ["Défenses immunitaires basses", "Récupération lente"],
            'ANALGESIQUE': ["Douleurs modérées à sévères", "Céphalées persistantes"],
            'BRONCHODILATATEUR': ["Gêne respiratoire", "Sibilances"]
        }
        
        return indications.get(traitement, ["Traitement symptomatique"])
    
    def _predire_retablissement(self, patient_data: Dict, analyse_sante: Dict, traitements: List[Dict]) -> Dict:
        """Prédit le rétablissement du patient"""
        
        if not traitements:
            return self._prediction_defaut(patient_data)
        
        meilleur_traitement = traitements[0]
        
        # Calcul de la durée prédite
        duree_predite = self._predire_duree_maladie(
            patient_data.get('pathologie', ''),
            analyse_sante['score_gravite'],
            analyse_sante['resilience_patient'],
            meilleur_traitement['score_global'],
            patient_data.get('profil', {})
        )
        
        # Calcul de la probabilité de succès
        probabilite_succes = self._calculer_probabilite_succes(
            analyse_sante,
            meilleur_traitement,
            patient_data.get('profil', {})
        )
        
        # Date de rétablissement prédite
        date_predite = datetime.now() + timedelta(days=duree_predite)
        
        # Évolution prédite
        evolution_predite = self._predire_evolution(analyse_sante, duree_predite)
        
        return {
            'duree_maladie_predite': duree_predite,
            'date_retablissement_predite': date_predite.isoformat(),
            'probabilite_succes': probabilite_succes,
            'niveau_confiance': self._calculer_confiance_prediction(analyse_sante, traitements),
            'facteurs_favorables': self._identifier_facteurs_favorables(analyse_sante),
            'risques_identifies': self._identifier_risques(analyse_sante, patient_data.get('profil', {})),
            'evolution_predite': evolution_predite,
            'recommandations_specifiques': self._generer_recommandations_specifiques(analyse_sante, probabilite_succes)
        }
    
    def _predire_duree_maladie(self, pathologie: str, gravite: float, resilience: float, efficacite_traitement: float, profil: Dict) -> int:
        """Prédit la durée de la maladie"""
        patho_ref = self.base_connaissances_medicales['pathologies_reference'].get(
            pathologie.upper(),
            {'duree_moyenne': 10, 'severite_base': 0.5}
        )
        
        duree_base = patho_ref['duree_moyenne']
        
        # Ajustements basés sur les facteurs individuels
        ajustement_gravite = gravite * 0.5  # +50% pour gravité élevée
        ajustement_resilience = (1 - resilience) * 0.3  # -30% pour résilience élevée
        ajustement_traitement = (1 - efficacite_traitement) * 0.4  # -40% pour traitement efficace
        ajustement_age = 0.2 if profil.get('age', 40) >= 65 else 0  # +20% pour les seniors
        ajustement_comorbidities = min(profil.get('comorbidities', 0) * 0.1, 0.3)  # +10% par comorbidité
        
        duree_ajustee = duree_base * (
            1 + 
            ajustement_gravite - 
            ajustement_resilience - 
            ajustement_traitement + 
            ajustement_age + 
            ajustement_comorbidities
        )
        
        return max(1, int(duree_ajustee))
    
    def _calculer_probabilite_succes(self, analyse_sante: Dict, traitement: Dict, profil: Dict) -> float:
        """Calcule la probabilité de succès du traitement"""
        facteurs = []
        
        # Potentiel de rétablissement naturel
        facteurs.append(analyse_sante['potentiel_retablissement'])
        
        # Efficacité du traitement
        facteurs.append(traitement['score_global'])
        
        # Résilience du patient
        facteurs.append(analyse_sante['resilience_patient'])
        
        # Harmonnie biologique
        facteurs.append(analyse_sante['harmonie_biologique'])
        
        # Facteur profil
        age_group = self._determiner_groupe_age(profil.get('age', 40))
        profil_ref = self.base_connaissances_medicales['profils_patients'].get(
            age_group,
            {'recuperation': 0.7}
        )
        facteurs.append(profil_ref['recuperation'])
        
        probabilite = sum(facteurs) / len(facteurs)
        
        # Ajustements contextuels
        if analyse_sante['score_gravite'] > 0.8:
            probabilite *= 0.8  # Réduction pour cas graves
        elif analyse_sante['score_gravite'] < 0.3:
            probabilite *= 1.1  # Augmentation pour cas légers
        
        if profil.get('comorbidities', 0) >= 2:
            probabilite *= 0.9  # Réduction pour comorbidités multiples
        
        return min(max(probabilite, 0), 1)
    
    def _calculer_confiance_prediction(self, analyse_sante: Dict, traitements: List[Dict]) -> float:
        """Calcule le niveau de confiance de la prédiction"""
        facteurs = []
        
        # Stabilité de l'analyse
        facteurs.append(analyse_sante['harmonie_biologique'])
        
        # Qualité des traitements disponibles
        if traitements:
            meilleur_score = max(t['score_global'] for t in traitements)
            facteurs.append(meilleur_score)
        else:
            facteurs.append(0.3)
        
        # Cohérence des données
        facteurs.append(1.0 - analyse_sante['score_gravite'] * 0.3)
        
        # Stabilité structurelle
        facteurs.append(1.0 if self._evaluer_stabilite_structurelle(analyse_sante['pyramide_sante']) else 0.7)
        
        return sum(facteurs) / len(facteurs)
    
    def _evaluer_stabilite_structurelle(self, pyramide: Dict) -> bool:
        """Évalue la stabilité structurelle de la pyramide de santé"""
        if not pyramide['inferieure']:
            return True
        
        base_finale = pyramide['inferieure'][-1]
        # Considérer stable si peu de variations dans la base finale
        return len(set(base_finale)) <= 2
    
    def _predire_evolution(self, analyse_sante: Dict, duree: int) -> List[Dict]:
        """Prédit l'évolution jour par jour"""
        evolution = []
        score_initial = analyse_sante['score_gravite']
        resilience = analyse_sante['resilience_patient']
        
        for jour in range(duree + 1):  # +1 pour inclure le jour 0
            if jour == 0:
                score = score_initial
            else:
                # Modèle d'amélioration exponentielle
                amelioration_jour = resilience * 0.15
                score = max(0, score_initial * (0.9 ** jour) - (amelioration_jour * jour))
            
            etat = self._determiner_etat_from_score(score)
            
            evolution.append({
                'jour': jour,
                'score_gravite': max(0, min(score, 1)),
                'etat': etat,
                'actions_recommandees': self._generer_actions_jour(jour, etat, score)
            })
        
        return evolution
    
    def _determiner_etat_from_score(self, score: float) -> str:
        """Détermine l'état de santé à partir d'un score"""
        if score >= 0.8:
            return "CRITIQUE"
        elif score >= 0.6:
            return "GRAVE"
        elif score >= 0.4:
            return "MODÉRÉ"
        elif score >= 0.2:
            return "STABLE"
        else:
            return "BON"
    
    def _generer_actions_jour(self, jour: int, etat: str, score: float) -> List[str]:
        """Génère les actions recommandées pour un jour donné"""
        actions_base = ["Surveillance des symptômes", "Hydratation adéquate"]
        
        if jour == 0:
            actions_base.extend(["Début du traitement", "Repos strict"])
        elif etat in ["CRITIQUE", "GRAVE"]:
            actions_base.extend(["Surveillance médicale rapprochée", "Contrôle des paramètres vitaux"])
        elif etat == "MODÉRÉ":
            actions_base.extend(["Repos relatif", "Adaptation des activités"])
        elif score < 0.3:
            actions_base.extend(["Reprise progressive des activités", "Réadaptation"])
        
        if jour % 3 == 0:  # Tous les 3 jours
            actions_base.append("Évaluation de l'évolution")
        
        return actions_base
    
    def _prediction_defaut(self, patient_data: Dict) -> Dict:
        """Retourne une prédiction par défaut en cas de données insuffisantes"""
        date_predite = datetime.now() + timedelta(days=14)
        
        return {
            'duree_maladie_predite': 14,
            'date_retablissement_predite': date_predite.isoformat(),
            'probabilite_succes': 0.5,
            'niveau_confiance': 0.3,
            'facteurs_favorables': ['Données insuffisantes pour une analyse précise'],
            'risques_identifies': ['Traitement non spécifique recommandé'],
            'evolution_predite': [],
            'recommandations_specifiques': ['Consultation médicale recommandée pour affiner le diagnostic']
        }
    
    def _identifier_facteurs_favorables(self, analyse_sante: Dict) -> List[str]:
        """Identifie les facteurs favorables au rétablissement"""
        facteurs = []
        
        if analyse_sante['resilience_patient'] > 0.7:
            facteurs.append("Forte résilience du patient")
        
        if analyse_sante['harmonie_biologique'] > 0.8:
            facteurs.append("Harmonie biologique élevée")
        
        if analyse_sante['potentiel_retablissement'] > 0.7:
            facteurs.append("Potentiel de rétablissement élevé")
        
        if analyse_sante['score_gravite'] < 0.4:
            facteurs.append("Gravité modérée de la condition")
        
        if not facteurs:
            facteurs.append("Analyse en cours - facteurs à déterminer")
        
        return facteurs
    
    def _identifier_risques(self, analyse_sante: Dict, profil: Dict) -> List[str]:
        """Identifie les risques potentiels"""
        risques = []
        
        if analyse_sante['score_gravite'] > 0.7:
            risques.append("Condition médicale sévère")
        
        if analyse_sante['resilience_patient'] < 0.4:
            risques.append("Faible résilience du patient")
        
        if analyse_sante['harmonie_biologique'] < 0.5:
            risques.append("Déséquilibre biologique détecté")
        
        if profil.get('comorbidities', 0) > 2:
            risques.append("Multiples comorbidités")
        
        if profil.get('age', 40) >= 65:
            risques.append("Âge avancé (facteur de risque)")
        
        if not risques:
            risques.append("Risques modérés - surveillance standard recommandée")
        
        return risques
    
    def _generer_recommandations_specifiques(self, analyse_sante: Dict, probabilite_succes: float) -> List[str]:
        """Génère des recommandations spécifiques basées sur l'analyse"""
        recommandations = []
        
        if analyse_sante['resilience_patient'] < 0.5:
            recommandations.append("Renforcement du système immunitaire recommandé")
        
        if analyse_sante['harmonie_biologique'] < 0.6:
            recommandations.append("Approche holistique pour rétablir l'équilibre biologique")
        
        if probabilite_succes < 0.6:
            recommandations.append("Plan de contingence à prévoir")
            recommandations.append("Surveillance renforcée nécessaire")
        
        if analyse_sante['etat_sante'] in [EtatSante.CRITIQUE, EtatSante.GRAVE]:
            recommandations.append("Prise en charge médicale spécialisée recommandée")
        
        return recommandations
    
    def _identifier_facteurs_pronostiques(self, analyse_sante: Dict, patient_data: Dict) -> Dict:
        """Identifie les facteurs pronostiques importants"""
        return {
            'facteur_cle_resilience': analyse_sante['resilience_patient'],
            'facteur_cle_harmonie': analyse_sante['harmonie_biologique'],
            'facteur_cle_gravite': analyse_sante['score_gravite'],
            'indicateur_retablissement': analyse_sante['potentiel_retablissement'],
            'etat_sante_global': analyse_sante['etat_sante'].label,
            'score_pronostic_global': (
                analyse_sante['potentiel_retablissement'] * 0.4 +
                (1 - analyse_sante['score_gravite']) * 0.3 +
                analyse_sante['resilience_patient'] * 0.3
            ),
            'facteurs_aggravants': len(analyse_sante['facteurs_aggravants']),
            'indicateurs_favorables': len(analyse_sante['indicateurs_favorables'])
        }
    
    def _generer_plan_soins(self, prediction: Dict, traitements: List[Dict], patient_data: Dict) -> Dict:
        """Génère un plan de soins personnalisé"""
        if not traitements:
            return self._plan_soins_defaut()
        
        meilleur_traitement = traitements[0]
        
        return {
            'traitement_principal': meilleur_traitement['nom'],
            'protocole_applique': meilleur_traitement['protocole'],
            'duree_traitement_recommandee': prediction['duree_maladie_predite'],
            'posologie_recommandee': self._determiner_posologie(meilleur_traitement['nom'], patient_data),
            'suivi_recommande': self._generer_calendrier_suivi(prediction['duree_maladie_predite'], prediction['evolution_predite']),
            'criteres_amelioration': self._definir_criteres_amelioration(patient_data),
            'actions_immediates': self._definir_actions_immediates(prediction['probabilite_succes'], patient_data),
            'contingence': self._prevoir_contingence(traitements, prediction),
            'recommandations_complementaires': self._generer_recommandations_complementaires(patient_data)
        }
    
    def _determiner_posologie(self, traitement: str, patient_data: Dict) -> str:
        """Détermine la posologie recommandée"""
        posologies = {
            'ANTIVIRAL': "1 comprimé 2 fois par jour pendant 5 jours",
            'ANTIBIOTIQUE': "1 comprimé 3 fois par jour pendant 7-10 jours",
            'ANTIINFLAMMATOIRE': "1 comprimé 2-3 fois par jour selon la douleur",
            'IMMUNOSTIMULANT': "1 dose par jour pendant 10 jours",
            'ANALGESIQUE': "1-2 comprimés selon l'intensité de la douleur",
            'BRONCHODILATATEUR': "2 inhalations 4 fois par jour"
        }
        
        base_posologie = posologies.get(traitement, "Selon prescription médicale")
        
        # Ajustement pour les seniors
        if patient_data.get('profil', {}).get('age', 40) >= 65:
            if traitement in ['ANTIBIOTIQUE', 'ANTIINFLAMMATOIRE']:
                return base_posologie + " (dose adaptée pour senior)"
        
        return base_posologie
    
    def _generer_calendrier_suivi(self, duree: int, evolution: List[Dict]) -> List[Dict]:
        """Génère un calendrier de suivi personnalisé"""
        calendrier = []
        
        # Points de contrôle stratégiques
        points_controle = self._determiner_points_controle(duree, evolution)
        
        for point in points_controle:
            etat_jour = next((e for e in evolution if e['jour'] == point), None)
            if etat_jour:
                calendrier.append({
                    'jour': point,
                    'objectif': self._definir_objectif_jour(point, etat_jour['etat']),
                    'actions': etat_jour['actions_recommandees'],
                    'critères_evaluation': self._definir_criteres_evaluation(point)
                })
        
        return calendrier
    
    def _determiner_points_controle(self, duree: int, evolution: List[Dict]) -> List[int]:
        """Détermine les points de contrôle optimaux"""
        if duree <= 3:
            return list(range(1, duree + 1))
        elif duree <= 7:
            return [1, 3, duree]
        else:
            return [1, 3, 7, duree//2, duree]
    
    def _definir_objectif_jour(self, jour: int, etat: str) -> str:
        """Définit l'objectif pour un jour donné"""
        objectifs = {
            'CRITIQUE': "Stabilisation de l'état",
            'GRAVE': "Amélioration des symptômes principaux",
            'MODÉRÉ': "Réduction de l'intensité des symptômes",
            'STABLE': "Consolidation de l'amélioration",
            'BON': "Récupération complète"
        }
        
        objectif_base = objectifs.get(etat, "Amélioration continue")
        
        if jour == 1:
            return f"J1: {objectif_base}"
        elif jour <= 3:
            return f"J{jour}: Évaluation de la réponse au traitement"
        else:
            return f"J{jour}: {objectif_base}"
    
    def _definir_criteres_evaluation(self, jour: int) -> List[str]:
        """Définit les critères d'évaluation pour un point de contrôle"""
        criteres_base = [
            "Intensité des symptômes",
            "Paramètres vitaux",
            "Tolérance au traitement"
        ]
        
        if jour >= 3:
            criteres_base.extend(["Amélioration fonctionnelle", "Qualité de vie"])
        
        if jour >= 7:
            criteres_base.append("Prévention des complications")
        
        return criteres_base
    
    def _definir_criteres_amelioration(self, patient_data: Dict) -> List[str]:
        """Définit les critères d'amélioration à surveiller"""
        pathologie = patient_data.get('pathologie', '').upper()
        criteres_generaux = [
            "Réduction de l'intensité des symptômes",
            "Amélioration des paramètres vitaux",
            "Retour de l'appétit et du sommeil",
            "Augmentation du niveau d'énergie"
        ]
        
        criteres_specifiques = {
            'GRIPPE': ["Disparition de la fièvre", "Amélioration de l'état général"],
            'COVID': ["Amélioration respiratoire", "Retour de l'odorat/goût"],
            'BRONCHITE': ["Diminution de la toux", "Amélioration de l'expectoration"],
            'PNEUMONIE': ["Normalisation radiologique", "Disparition des crépitements"],
            'MIGRAINE': ["Cessation des céphalées", "Reprise des activités normales"]
        }
        
        return criteres_generaux + criteres_specifiques.get(pathologie, [])
    
    def _definir_actions_immediates(self, probabilite_succes: float, patient_data: Dict) -> List[str]:
        """Définit les actions immédiates basées sur la probabilité de succès"""
        actions = [
            "Mise en place du traitement recommandé",
            "Surveillance des paramètres clés",
            "Information du patient sur le plan de soins"
        ]
        
        if probabilite_succes < 0.7:
            actions.append("Préparation d'un plan de contingence")
            actions.append("Surveillance renforcée des premiers jours")
        
        if probabilite_succes < 0.5:
            actions.append("Consultation spécialisée recommandée")
            actions.append("Évaluation hospitalière à considérer")
        
        # Actions spécifiques selon la pathologie
        pathologie = patient_data.get('pathologie', '').upper()
        if pathologie in ['COVID', 'PNEUMONIE']:
            actions.append("Surveillance oxymétrie pulsée")
        if pathologie == 'MIGRAINE':
            actions.append("Environnement calme et obscurité")
        
        return actions
    
    def _prevoir_contingence(self, traitements: List[Dict], prediction: Dict) -> Dict:
        """Prévoit un plan de contingence"""
        if len(traitements) > 1:
            traitement_alternatif = traitements[1]
            return {
                'traitement_alternatif': traitement_alternatif['nom'],
                'declenchement': f"Si absence d'amélioration après {min(3, prediction['duree_maladie_predite']//2)} jours",
                'conditions_activation': [
                    "Aggravation des symptômes",
                    "Apparition de nouveaux symptômes",
                    "Absence d'amélioration après délai défini"
                ],
                'actions': ["Réévaluation complète", "Changement de protocole", "Consultation médicale"]
            }
        else:
            return {
                'traitement_alternatif': "Soins de support standards",
                'declenchement': "Si détérioration de l'état à tout moment",
                'conditions_activation': [
                    "Aggravation significative",
                    "Apparition de signes de complication"
                ],
                'actions': ["Consultation médicale urgente", "Révision du diagnostic", "Prise en charge spécialisée"]
            }
    
    def _generer_recommandations_complementaires(self, patient_data: Dict) -> List[str]:
        """Génère des recommandations complémentaires"""
        recommandations = [
            "Repos adapté à l'état de santé",
            "Hydratation suffisante",
            "Alimentation équilibrée et adaptée"
        ]
        
        pathologie = patient_data.get('pathologie', '').upper()
        if pathologie in ['GRIPPE', 'COVID']:
            recommandations.append("Isolement pour prévention de la transmission")
        if pathologie in ['BRONCHITE', 'PNEUMONIE']:
            recommandations.append("Éviction des facteurs irritants respiratoires")
        if pathologie == 'MIGRAINE':
            recommandations.append("Gestion du stress et des facteurs déclenchants")
        
        # Recommandations selon l'âge
        age = patient_data.get('profil', {}).get('age', 40)
        if age >= 65:
            recommandations.append("Surveillance particulière des chutes")
            recommandations.append("Adaptation de l'environnement")
        
        return recommandations
    
    def _plan_soins_defaut(self) -> Dict:
        """Retourne un plan de soins par défaut"""
        return {
            'traitement_principal': "Soins symptomatiques",
            'protocole_applique': "PROTOCOLE_STANDARD",
            'duree_traitement_recommandee': 7,
            'posologie_recommandee': "Selon symptômes",
            'suivi_recommande': [{'jour': 3, 'actions': ["Évaluation de l'état général"]}],
            'criteres_amelioration': ["Réduction des symptômes principaux"],
            'actions_immediates': ["Repos", "Hydratation", "Surveillance"],
            'contingence': {'actions': ["Consulter en cas d'aggravation"]},
            'recommandations_complementaires': ["Consultation médicale pour diagnostic précis"]
        }
    
    def _generer_recommandations_suivi(self, prediction: Dict, patient_data: Dict) -> List[str]:
        """Génère des recommandations de suivi"""
        recommandations = [
            f"Suivi médical pendant {prediction['duree_maladie_predite']} jours",
            "Signalement immédiat de toute aggravation",
            "Respect strict du traitement prescrit",
            "Tenue d'un journal des symptômes"
        ]
        
        if prediction['probabilite_succes'] < 0.7:
            recommandations.append("Surveillance rapprochée recommandée")
            recommandations.append("Prévoir une consultation de contrôle à J+3")
        
        if prediction['probabilite_succes'] < 0.5:
            recommandations.append("Envisager une hospitalisation si état stationnaire")
            recommandations.append("Mise en place de soins de support intensifs")
        
        # Recommandations spécifiques
        if patient_data.get('profil', {}).get('comorbidities', 0) > 0:
            recommandations.append("Surveillance particulière des comorbidités")
        
        return recommandations
    
    def _calculer_confiance_globale(self, analyse_sante: Dict, prediction: Dict, traitements: List[Dict]) -> float:
        """Calcule le score de confiance global de l'analyse"""
        facteurs = []
        
        # Confiance dans l'analyse de l'état
        facteurs.append(analyse_sante['harmonie_biologique'])
        
        # Confiance dans les traitements
        if traitements:
            facteurs.append(max(t['score_global'] for t in traitements))
        else:
            facteurs.append(0.3)
        
        # Confiance dans la prédiction
        facteurs.append(prediction['niveau_confiance'])
        
        # Stabilité structurelle
        facteurs.append(1.0 if self._evaluer_stabilite_structurelle(analyse_sante['pyramide_sante']) else 0.7)
        
        # Cohérence globale
        coherence = 1.0 - abs(
            analyse_sante['potentiel_retablissement'] - 
            prediction['probabilite_succes']
        )
        facteurs.append(coherence)
        
        return sum(facteurs) / len(facteurs)
    
    def _generer_avertissements(self, analyse_sante: Dict, prediction: Dict) -> List[str]:
        """Génère des avertissements basés sur l'analyse"""
        avertissements = []
        
        if analyse_sante['etat_sante'] in [EtatSante.CRITIQUE, EtatSante.GRAVE]:
            avertissements.append("État de santé préoccupant - surveillance médicale requise")
        
        if prediction['probabilite_succes'] < 0.4:
            avertissements.append("Pronostic réservé - nécessité d'une prise en charge spécialisée")
        
        if len(analyse_sante['facteurs_aggravants']) >= 3:
            avertissements.append("Multiples facteurs de risque - vigilance accrue nécessaire")
        
        if analyse_sante['resilience_patient'] < 0.3:
            avertissements.append("Faible résilience détectée - récupération potentiellement prolongée")
        
        return avertissements
    
    def generer_rapport_medical(self, patient_data: Dict) -> str:
        """Génère un rapport médical complet"""
        analyse = self.analyser_patient(patient_data)
        
        rapport = f"""
╔═══════════════════════════════════════╗
║        RAPPORT MÉDICAL ALGO VÉRITÉ   ║
║      Système Prédictif Sanitaire     ║
╚═══════════════════════════════════════╝

PATIENT: {analyse['patient_id']}
DATE ANALYSE: {analyse['timestamp_analyse']}
CONFIDENCE GLOBALE: {analyse['score_confiance_global']:.1%}

CONDITION ACTUELLE
──────────────────
• État de santé: {analyse['condition_actuelle']['etat_sante'].label}
• Score de gravité: {analyse['condition_actuelle']['score_gravite']:.3f}
• Potentiel de rétablissement: {analyse['condition_actuelle']['potentiel_retablissement']:.1%}
• Résilience patient: {analyse['condition_actuelle']['resilience_patient']:.3f}
• Harmonie biologique: {analyse['condition_actuelle']['harmonie_biologique']:.3f}

TRAITEMENTS RECOMMANDÉS
───────────────────────
"""
        for i, traitement in enumerate(analyse['traitements_recommandes'], 1):
            rapport += f"{i}. {traitement['nom']} (Score: {traitement['score_global']:.3f})\n"
            rapport += f"   • Protocole: {traitement['protocole']}\n"
            rapport += f"   • Efficacité: {traitement['efficacite_base']:.1%}\n"
            rapport += f"   • Compatibilité: {traitement['compatibilite_personnalisee']:.1%}\n"
        
        rapport += f"""
PRÉDICTION DE RÉTABLISSEMENT
────────────────────────────
• Durée maladie prédite: {analyse['prediction_retablissement']['duree_maladie_predite']} jours
• Date rétablissement: {analyse['prediction_retablissement']['date_retablissement_predite'][:10]}
• Probabilité succès: {analyse['prediction_retablissement']['probabilite_succes']:.1%}
• Niveau confiance: {analyse['prediction_retablissement']['niveau_confiance']:.1%}

FACTEURS FAVORABLES
───────────────────
"""
        for facteur in analyse['prediction_retablissement']['facteurs_favorables']:
            rapport += f"• {facteur}\n"
        
        rapport += f"""
RISQUES IDENTIFIÉS
──────────────────
"""
        for risque in analyse['prediction_retablissement']['risques_identifies']:
            rapport += f"• {risque}\n"
        
        rapport += f"""
PLAN DE SOINS
─────────────
• Traitement principal: {analyse['plan_soins_personnalise']['traitement_principal']}
• Protocole: {analyse['plan_soins_personnalise']['protocole_applique']}
• Durée: {analyse['plan_soins_personnalise']['duree_traitement_recommandee']} jours
• Posologie: {analyse['plan_soins_personnalise']['posologie_recommandee']}

ACTIONS IMMÉDIATES
──────────────────
"""
        for action in analyse['plan_soins_personnalise']['actions_immediates']:
            rapport += f"• {action}\n"
        
        if analyse['avertissements']:
            rapport += f"""
⚠️  AVERTISSEMENTS
────────────────
"""
            for avertissement in analyse['avertissements']:
                rapport += f"• {avertissement}\n"
        
        rapport += f"""
════════════════════════════════════════
         RAPPORT MÉDICAL TERMINÉ
════════════════════════════════════════
"""
        return rapport

    def analyser_cohorte(self, patients_data: List[Dict]) -> Dict:
        """Analyse une cohorte de patients pour la recherche"""
        analyses = []
        
        for patient_data in patients_data:
            try:
                analyse = self.analyser_patient(patient_data)
                analyses.append(analyse)
            except Exception as e:
                analyses.append({
                    'patient_id': patient_data.get('id', 'INCONNU'),
                    'erreur': str(e),
                    'statut': 'ÉCHEC_ANALYSE'
                })
        
        # Statistiques de la cohorte
        analyses_reussies = [a for a in analyses if 'erreur' not in a]
        
        if analyses_reussies:
            durees_moyennes = np.mean([a['prediction_retablissement']['duree_maladie_predite'] 
                                     for a in analyses_reussies])
            succes_moyen = np.mean([a['prediction_retablissement']['probabilite_succes'] 
                                  for a in analyses_reussies])
            confiance_moyenne = np.mean([a['prediction_retablissement']['niveau_confiance'] 
                                       for a in analyses_reussies])
        else:
            durees_moyennes = succes_moyen = confiance_moyenne = 0
        
        return {
            'cohorte_analyse': {
                'total_patients': len(patients_data),
                'analyses_reussies': len(analyses_reussies),
                'taux_reussite': len(analyses_reussies) / len(patients_data),
                'duree_maladie_moyenne': durees_moyennes,
                'probabilite_succes_moyenne': succes_moyen,
                'confiance_moyenne': confiance_moyenne
            },
            'analyses_detaillees': analyses,
            'recommandations_cohorte': self._generer_recommandations_cohorte(analyses_reussies)
        }
    
    def _generer_recommandations_cohorte(self, analyses: List[Dict]) -> List[str]:
        """Génère des recommandations pour la cohorte"""
        if not analyses:
            return ["Données insuffisantes pour générer des recommandations"]
        
        recommandations = []
        
        # Analyse des traitements les plus efficaces
        traitements_scores = {}
        for analyse in analyses:
            for traitement in analyse.get('traitements_recommandes', []):
                nom = traitement['nom']
                if nom not in traitements_scores:
                    traitements_scores[nom] = []
                traitements_scores[nom].append(traitement['score_global'])
        
        if traitements_scores:
            meilleur_traitement = max(traitements_scores.items(), key=lambda x: np.mean(x[1]))
            recommandations.append(f"Traitement le plus efficace: {meilleur_traitement[0]} (score moyen: {np.mean(meilleur_traitement[1]):.3f})")
        
        # Recommandations basées sur la gravité moyenne
        gravite_moyenne = np.mean([a['condition_actuelle']['score_gravite'] for a in analyses])
        if gravite_moyenne > 0.7:
            recommandations.append("Cohorte à haut risque - surveillance intensive recommandée")
        elif gravite_moyenne < 0.3:
            recommandations.append("Cohorte à faible risque - prise en charge standard adaptée")
        
        return recommandations