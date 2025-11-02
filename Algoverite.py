import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta
from enum import Enum
import hashlib

class EtatSante(Enum):
    CRITIQUE = 0.1
    GRAVE = 0.3
    MODERE = 0.6
    STABLE = 0.8
    EXCELLENT = 0.95

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
                'GRIPPE': {'severite_base': 0.4, 'duree_moyenne': 7, 'resilience': 0.8},
                'COVID': {'severite_base': 0.7, 'duree_moyenne': 14, 'resilience': 0.6},
                'BRONCHITE': {'severite_base': 0.5, 'duree_moyenne': 10, 'resilience': 0.7},
                'PNEUMONIE': {'severite_base': 0.8, 'duree_moyenne': 21, 'resilience': 0.5},
                'MIGRAINE': {'severite_base': 0.3, 'duree_moyenne': 2, 'resilience': 0.9}
            },
            'traitements_reference': {
                'ANTIVIRAL': {'efficacite': 0.7, 'delai_action': 2, 'compatibilite': 0.8},
                'ANTIBIOTIQUE': {'efficacite': 0.8, 'delai_action': 3, 'compatibilite': 0.7},
                'ANTIINFLAMMATOIRE': {'efficacite': 0.6, 'delai_action': 1, 'compatibilite': 0.9},
                'IMMUNOSTIMULANT': {'efficacite': 0.5, 'delai_action': 5, 'compatibilite': 0.95},
                'ANALGESIQUE': {'efficacite': 0.4, 'delai_action': 1, 'compatibilite': 0.85}
            },
            'profils_patients': {
                'JEUNE': {'resilience': 0.9, 'reponse_traitement': 0.8, 'recuperation': 0.85},
                'ADULTE': {'resilience': 0.7, 'reponse_traitement': 0.7, 'recuperation': 0.7},
                'SENIOR': {'resilience': 0.5, 'reponse_traitement': 0.6, 'recuperation': 0.5},
                'IMMUNODEPRIME': {'resilience': 0.3, 'reponse_traitement': 0.4, 'recuperation': 0.3}
            }
        }
    
    def _initialiser_protocoles(self) -> Dict:
        """Initialise les protocoles de traitement optimisés"""
        return {
            'PROTOCOLE_STANDARD': {
                'pathologies': ['GRIPPE', 'BRONCHITE'],
                'traitements': ['ANTIVIRAL', 'ANTIINFLAMMATOIRE'],
                'duree_moyenne': 7,
                'efficacite_attendue': 0.75
            },
            'PROTOCOLE_INTENSIF': {
                'pathologies': ['COVID', 'PNEUMONIE'],
                'traitements': ['ANTIBIOTIQUE', 'ANTIINFLAMMATOIRE', 'IMMUNOSTIMULANT'],
                'duree_moyenne': 14,
                'efficacite_attendue': 0.65
            },
            'PROTOCOLE_LEGER': {
                'pathologies': ['MIGRAINE'],
                'traitements': ['ANALGESIQUE'],
                'duree_moyenne': 2,
                'efficacite_attendue': 0.85
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
        # Analyse pyramidale de la condition du patient
        analyse_sante = self._analyser_condition_patient(patient_data)
        
        # Recherche de traitement optimal
        traitements_recommandes = self._rechercher_traitements_optimaux(patient_data, analyse_sante)
        
        # Prédiction de rétablissement
        prediction = self._predire_retablissement(patient_data, analyse_sante, traitements_recommandes)
        
        # Génération du plan de soins
        plan_soins = self._generer_plan_soins(prediction, traitements_recommandes)
        
        resultat = {
            'patient_id': patient_data.get('id', 'ANONYME'),
            'timestamp_analyse': datetime.now().isoformat(),
            'condition_actuelle': analyse_sante,
            'traitements_recommandes': traitements_recommandes,
            'prediction_retablissement': prediction,
            'plan_soins_personnalise': plan_soins,
            'facteurs_pronostiques': self._identifier_facteurs_pronostiques(analyse_sante),
            'recommandations_suivi': self._generer_recommandations_suivi(prediction)
        }
        
        # Archivage
        self.historique_patients[patient_data.get('id', 'ANONYME')] = resultat
        
        return resultat
    
    def _analyser_condition_patient(self, patient_data: Dict) -> Dict:
        """Analyse la condition médicale du patient via l'algorithme pyramidal"""
        
        # Conversion des symptômes en séquence numérique
        symptomes_codes = self._coder_symptomes(patient_data.get('symptomes', []))
        pathologie_codes = self._coder_pathologie(patient_data.get('pathologie', ''))
        profil_codes = self._coder_profil_patient(patient_data.get('profil', {}))
        
        # Construction de la pyramide de santé
        pyramide_sante = self._construire_pyramide_sante(symptomes_codes, pathologie_codes, profil_codes)
        
        return {
            'pyramide_sante': pyramide_sante,
            'score_gravite': self._calculer_gravite(symptomes_codes, pathologie_codes),
            'potentiel_retablissement': self._evaluer_potentiel_retablissement(pyramide_sante),
            'resilience_patient': self._calculer_resilience(profil_codes, pyramide_sante),
            'harmonie_biologique': self._evaluer_harmonie_biologique(pyramide_sante)
        }
    
    def _coder_symptomes(self, symptomes: List[str]) -> List[int]:
        """Code les symptômes en séquence numérique"""
        if not symptomes:
            return [0]
        
        codes = []
        for symptome in symptomes:
            # Conversion du symptôme en code numérique unique
            code = sum(ord(c) for c in symptome.upper()) % 100
            codes.append(code)
        
        return codes if codes else [0]
    
    def _coder_pathologie(self, pathologie: str) -> List[int]:
        """Code la pathologie en séquence numérique"""
        if not pathologie:
            return [0]
        
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
        age_group = profil.get('age_group', 'ADULTE')
        comorbidities = profil.get('comorbidities', 0)
        immunity_level = profil.get('immunity_level', 0.7)
        
        profil_ref = self.base_connaissances_medicales['profils_patients'].get(
            age_group.upper(),
            {'resilience': 0.7, 'reponse_traitement': 0.7, 'recuperation': 0.7}
        )
        
        return [
            int(profil_ref['resilience'] * 100),
            int(profil_ref['reponse_traitement'] * 100),
            int(immunity_level * 100),
            comorbidities * 10
        ]
    
    def _construire_pyramide_sante(self, symptomes: List[int], pathologie: List[int], profil: List[int]) -> Dict:
        """Construit la pyramide de santé du patient"""
        
        # Base: combinaison des trois dimensions
        base = symptomes + pathologie + profil
        
        pyramide = {
            'base': base,
            'supérieure': [],
            'inférieure': []
        }
        
        # Construction partie supérieure (indicateurs d'amélioration)
        current = base
        while len(current) > 1:
            next_level = [current[i] + current[i+1] for i in range(len(current)-1)]
            pyramide['supérieure'].insert(0, next_level)
            current = next_level
        
        # Construction partie inférieure (indicateurs de risque)
        current = base
        while len(current) > 1:
            next_level = [abs(current[i] - current[i+1]) for i in range(len(current)-1)]
            pyramide['inférieure'].append(next_level)
            current = next_level
        
        return pyramide
    
    def _calculer_gravite(self, symptomes: List[int], pathologie: List[int]) -> float:
        """Calcule le score de gravité de la condition"""
        if not symptomes or not pathologie:
            return 0.5
        
        severite_symptomes = sum(symptomes) / (len(symptomes) * 100) if symptomes else 0
        severite_pathologie = pathologie[0] / 100 if pathologie else 0.5
        
        return min(max((severite_symptomes + severite_pathologie) / 2, 0), 1)
    
    def _evaluer_potentiel_retablissement(self, pyramide: Dict) -> float:
        """Évalue le potentiel de rétablissement du patient"""
        if not pyramide['supérieure'] or not pyramide['inférieure']:
            return 0.5
        
        # Ratio d'harmonie entre amélioration et risques
        sommet = pyramide['supérieure'][0][0] if pyramide['supérieure'] else 0
        base_risque = pyramide['inférieure'][-1][0] if pyramide['inférieure'] else 1
        
        if base_risque == 0:
            base_risque = 1  # Éviter division par zéro
        
        harmonie = 1.0 - min(abs(sommet - base_risque) / max(sommet, base_risque), 1)
        
        # Facteur de stabilité
        stabilite = 1.0 - (len(pyramide['inférieure']) / (len(pyramide['base']) * 2))
        
        return (harmonie + stabilite) / 2
    
    def _calculer_resilience(self, profil: List[int], pyramide: Dict) -> float:
        """Calcule la résilience du patient"""
        resilience_base = profil[0] / 100 if profil else 0.5
        
        # Facteur structurel de la pyramide
        symetrie = 1.0 - (abs(len(pyramide['supérieure']) - len(pyramide['inférieure'])) / 
                          max(len(pyramide['supérieure']), len(pyramide['inférieure']), 1))
        
        return (resilience_base + symetrie) / 2
    
    def _evaluer_harmonie_biologique(self, pyramide: Dict) -> float:
        """Évalue l'harmonie biologique du patient"""
        if not pyramide['supérieure'] or not pyramide['inférieure']:
            return 0.5
        
        # Équilibre entre les systèmes
        valeurs_sup = [item for niveau in pyramide['supérieure'] for item in niveau]
        valeurs_inf = [item for niveau in pyramide['inférieure'] for item in niveau]
        
        if not valeurs_sup or not valeurs_inf:
            return 0.5
        
        moyenne_sup = sum(valeurs_sup) / len(valeurs_sup)
        moyenne_inf = sum(valeurs_inf) / len(valeurs_inf)
        
        if moyenne_sup == 0 or moyenne_inf == 0:
            return 0.5
        
        harmonie = 1.0 - abs(moyenne_sup - moyenne_inf) / max(moyenne_sup, moyenne_inf)
        return max(0, min(1, harmonie))
    
    def _rechercher_traitements_optimaux(self, patient_data: Dict, analyse_sante: Dict) -> List[Dict]:
        """Recherche les traitements optimaux pour le patient"""
        pathologie = patient_data.get('pathologie', '').upper()
        profil = patient_data.get('profil', {})
        
        traitements_candidats = []
        
        # Recherche dans les protocoles établis
        for protocole_nom, protocole in self.protocoles_traitements.items():
            if pathologie in protocole['pathologies']:
                for traitement_nom in protocole['traitements']:
                    traitement_ref = self.base_connaissances_medicales['treatments_reference'].get(
                        traitement_nom,
                        {'efficacite': 0.5, 'delai_action': 5, 'compatibilite': 0.5}
                    )
                    
                    # Calcul du score de compatibilité personnalisé
                    score_compatibilite = self._calculer_compatibilite_traitement(
                        traitement_ref, profil, analyse_sante
                    )
                    
                    traitements_candidats.append({
                        'nom': traitement_nom,
                        'protocole': protocole_nom,
                        'efficacite_base': traitement_ref['efficacite'],
                        'compatibilite_personnalisee': score_compatibilite,
                        'score_global': (traitement_ref['efficacite'] + score_compatibilite) / 2,
                        'delai_action_attendu': traitement_ref['delai_action']
                    })
        
        # Tri par score global décroissant
        traitements_candidats.sort(key=lambda x: x['score_global'], reverse=True)
        
        return traitements_candidats[:3]  # Retourne les 3 meilleurs traitements
    
    def _calculer_compatibilite_traitement(self, traitement: Dict, profil: Dict, analyse_sante: Dict) -> float:
        """Calcule la compatibilité personnalisée du traitement"""
        age_group = profil.get('age_group', 'ADULTE')
        profil_ref = self.base_connaissances_medicales['profils_patients'].get(
            age_group.upper(),
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
        
        return sum(facteurs) / len(facteurs)
    
    def _predire_retablissement(self, patient_data: Dict, analyse_sante: Dict, traitements: List[Dict]) -> Dict:
        """Prédit le rétablissement du patient"""
        
        if not traitements:
            return self._prediction_defaut()
        
        meilleur_traitement = traitements[0]
        
        # Calcul de la durée prédite
        duree_predite = self._predire_duree_maladie(
            patient_data.get('pathologie', ''),
            analyse_sante['score_gravite'],
            analyse_sante['resilience_patient'],
            meilleur_traitement['score_global']
        )
        
        # Calcul de la probabilité de succès
        probabilite_succes = self._calculer_probabilite_succes(
            analyse_sante,
            meilleur_traitement,
            patient_data.get('profil', {})
        )
        
        # Date de rétablissement prédite
        date_predite = datetime.now() + timedelta(days=duree_predite)
        
        return {
            'duree_maladie_predite': duree_predite,
            'date_retablissement_predite': date_predite.isoformat(),
            'probabilite_succes': probabilite_succes,
            'niveau_confiance': self._calculer_confiance_prediction(analyse_sante, traitements),
            'facteurs_favorables': self._identifier_facteurs_favorables(analyse_sante),
            'risques_identifies': self._identifier_risques(analyse_sante, patient_data.get('profil', {}))
        }
    
    def _predire_duree_maladie(self, pathologie: str, gravite: float, resilience: float, efficacite_traitement: float) -> int:
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
        
        duree_ajustee = duree_base * (1 + ajustement_gravite - ajustement_resilience - ajustement_traitement)
        
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
        age_group = profil.get('age_group', 'ADULTE')
        profil_ref = self.base_connaissances_medicales['profils_patients'].get(
            age_group.upper(),
            {'recuperation': 0.7}
        )
        facteurs.append(profil_ref['recuperation'])
        
        probabilite = sum(facteurs) / len(facteurs)
        
        # Ajustement pour les cas extrêmes
        if analyse_sante['score_gravite'] > 0.8:
            probabilite *= 0.8
        elif analyse_sante['score_gravite'] < 0.3:
            probabilite *= 1.2
        
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
        facteurs.append(1.0 - analyse_sante['score_gravite'] * 0.5)
        
        return sum(facteurs) / len(facteurs)
    
    def _prediction_defaut(self) -> Dict:
        """Retourne une prédiction par défaut en cas de données insuffisantes"""
        date_predite = datetime.now() + timedelta(days=14)
        
        return {
            'duree_maladie_predite': 14,
            'date_retablissement_predite': date_predite.isoformat(),
            'probabilite_succes': 0.5,
            'niveau_confiance': 0.3,
            'facteurs_favorables': ['Données insuffisantes pour une analyse précise'],
            'risques_identifies': ['Traitement non spécifique recommandé']
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
        
        if not risques:
            risques.append("Risques modérés - surveillance standard recommandée")
        
        return risques
    
    def _identifier_facteurs_pronostiques(self, analyse_sante: Dict) -> Dict:
        """Identifie les facteurs pronostiques importants"""
        return {
            'facteur_cle_resilience': analyse_sante['resilience_patient'],
            'facteur_cle_harmonie': analyse_sante['harmonie_biologique'],
            'facteur_cle_gravite': analyse_sante['score_gravite'],
            'indicateur_retablissement': analyse_sante['potentiel_retablissement'],
            'score_pronostic_global': (
                analyse_sante['potentiel_retablissement'] * 0.4 +
                (1 - analyse_sante['score_gravite']) * 0.3 +
                analyse_sante['resilience_patient'] * 0.3
            )
        }
    
    def _generer_plan_soins(self, prediction: Dict, traitements: List[Dict]) -> Dict:
        """Génère un plan de soins personnalisé"""
        if not traitements:
            return self._plan_soins_defaut()
        
        meilleur_traitement = traitements[0]
        
        return {
            'traitement_principal': meilleur_traitement['nom'],
            'duree_traitement_recommandee': prediction['duree_maladie_predite'],
            'protocole_applique': meilleur_traitement['protocole'],
            'suivi_recommandé': self._generer_calendrier_suivi(prediction['duree_maladie_predite']),
            'criteres_amelioration': self._definir_criteres_amelioration(),
            'actions_immediates': self._definir_actions_immediates(prediction['probabilite_succes']),
            'contingence': self._prevoir_contingence(traitements)
        }
    
    def _generer_calendrier_suivi(self, duree: int) -> List[Dict]:
        """Génère un calendrier de suivi personnalisé"""
        calendrier = []
        
        # Points de contrôle basés sur la durée
        points_controle = [1, 3, 7] if duree <= 7 else [1, 3, 7, 14, int(duree/2), duree]
        
        for jour in points_controle:
            if jour <= duree:
                calendrier.append({
                    'jour': jour,
                    'actions': [
                        "Évaluation des symptômes",
                        "Contrôle des paramètres vitaux",
                        "Ajustement traitement si nécessaire"
                    ]
                })
        
        return calendrier
    
    def _definir_criteres_amelioration(self) -> List[str]:
        """Définit les critères d'amélioration à surveiller"""
        return [
            "Réduction de l'intensité des symptômes",
            "Amélioration des paramètres vitaux",
            "Retour de l'appétit et du sommeil",
            "Augmentation du niveau d'énergie",
            "Normalisation des marqueurs biologiques"
        ]
    
    def _definir_actions_immediates(self, probabilite_succes: float) -> List[str]:
        """Définit les actions immédiates basées sur la probabilité de succès"""
        actions = ["Mise en place du traitement recommandé", "Surveillance des paramètres clés"]
        
        if probabilite_succes < 0.6:
            actions.append("Préparation d'un plan de contingence")
            actions.append("Surveillance renforcée")
        
        if probabilite_succes < 0.4:
            actions.append("Consultation spécialisée recommandée")
            actions.append("Évaluation hospitalière à considérer")
        
        return actions
    
    def _prevoir_contingence(self, traitements: List[Dict]) -> Dict:
        """Prévoit un plan de contingence"""
        if len(traitements) > 1:
            return {
                'traitement_alternatif': traitements[1]['nom'],
                'declenchement': "Si absence d'amélioration après 3 jours",
                'actions': ["Réévaluation complète", "Changement de protocole"]
            }
        else:
            return {
                'traitement_alternatif': "Soins de support standards",
                'declenchement': "Si détérioration de l'état",
                'actions': ["Consultation médicale urgente", "Révision du diagnostic"]
            }
    
    def _plan_soins_defaut(self) -> Dict:
        """Retourne un plan de soins par défaut"""
        return {
            'traitement_principal': "Soins symptomatiques",
            'duree_traitement_recommandee': 7,
            'protocole_applique': "PROTOCOLE_STANDARD",
            'suivi_recommandé': [{'jour': 3, 'actions': ["Évaluation de l'état général"]}],
            'criteres_amelioration': ["Réduction des symptômes principaux"],
            'actions_immediates': ["Repos", "Hydratation", "Surveillance"],
            'contingence': {'actions': ["Consulter en cas d'aggravation"]}
        }
    
    def _generer_recommandations_suivi(self, prediction: Dict) -> List[str]:
        """Génère des recommandations de suivi"""
        recommandations = [
            f"Suivi médical pendant {prediction['duree_maladie_predite']} jours",
            "Signalement immédiat de toute aggravation",
            "Respect strict du traitement prescrit"
        ]
        
        if prediction['probabilite_succes'] < 0.7:
            recommandations.append("Surveillance rapprochée recommandée")
            recommandations.append("Prévoir une consultation de contrôle à J+3")
        
        if prediction['probabilite_succes'] < 0.5:
            recommandations.append("Envisager une hospitalisation si état stationnaire")
            recommandations.append("Mise en place de soins de support intensifs")
        
        return recommandations
    
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

CONDITION ACTUELLE
──────────────────
• Score de gravité: {analyse['condition_actuelle']['score_gravite']:.3f}
• Potentiel de rétablissement: {analyse['condition_actuelle']['potentiel_retablissement']:.1%}
• Résilience patient: {analyse['condition_actuelle']['resilience_patient']:.3f}
• Harmonie biologique: {analyse['condition_actuelle']['harmonie_biologique']:.3f}

TRAITEMENTS RECOMMANDÉS
───────────────────────
"""
        for i, traitement in enumerate(analyse['traitements_recommandes'], 1):
            rapport += f"{i}. {traitement['nom']} (Score: {traitement['score_global']:.3f})\n"
        
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

ACTIONS IMMÉDIATES
──────────────────
"""
        for action in analyse['plan_soins_personnalise']['actions_immediates']:
            rapport += f"• {action}\n"
        
        rapport += f"""
════════════════════════════════════════
         RAPPORT MÉDICAL TERMINÉ
════════════════════════════════════════
"""
        return rapport

# Démonstration du système médical
def demo_systeme_medical():
    """Démonstration du système médical prédictif"""
    
    print("""
╔═══════════════════════════════════════╗
║    SYSTÈME MÉDICAL ALGO VÉRITÉ       ║
║   Recherche Sanitaire & Prédiction   ║
╚═══════════════════════════════════════╝
    """)
    
    algo_medical = AlgoVeriteMedical()
    
    # Cas de test
    patients_test = [
        {
            'id': 'PAT001',
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX', 'FATIGUE'],
            'profil': {'age_group': 'ADULTE', 'comorbidities': 1, 'immunity_level': 0.6}
        },
        {
            'id': 'PAT002', 
            'pathologie': 'COVID',
            'symptomes': ['FIÈVRE', 'TROUBLE_RESPIRATOIRE', 'ANOSMIE'],
            'profil': {'age_group': 'SENIOR', 'comorbidities': 3, 'immunity_level': 0.4}
        },
        {
            'id': 'PAT003',
            'pathologie': 'BRONCHITE',
            'symptomes': ['TOUX', 'EXPECTORATION'],
            'profil': {'age_group': 'JEUNE', 'comorbidities': 0, 'immunity_level': 0.8}
        }
    ]
    
    for patient in patients_test:
        print(f"\n{'='*60}")
        print(f"ANALYSE DU PATIENT: {patient['id']}")
        print(f"{'='*60}")
        
        rapport = algo_medical.generer_rapport_medical(patient)
        print(rapport)
        
        # Pause entre les analyses
        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    demo_systeme_medical()