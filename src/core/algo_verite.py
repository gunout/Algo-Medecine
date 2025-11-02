import hashlib
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime
from enum import Enum

class ComplexiteNiveau(Enum):
    SIMPLE = "SIMPLE"
    MODEREE = "MODÉRÉE"
    COMPLEXE = "COMPLEXE"
    TRES_COMPLEXE = "TRÈS COMPLEXE"

class AlgoVerite:
    """
    Algorithme d'analyse pyramidale révélant la structure mathématique
    et philosophique des données par construction/déconstruction
    """
    
    def __init__(self):
        self.archives_analyses = {}
        self.historique_operations = []
        
    def analyser_sequence(self, sequence: List[int], nom: str = "Sequence") -> Dict[str, Any]:
        """Analyse complète d'une séquence numérique"""
        
        if not sequence:
            raise ValueError("La séquence ne peut pas être vide")
        
        # Construction de la pyramide complète
        pyramide = self._construire_pyramide(sequence)
        
        # Calcul des signatures
        signatures = self._calculer_signatures(pyramide, nom)
        
        # Interprétation structurelle
        interpretation = self._interpreter_pyramide(pyramide, nom)
        
        resultat = {
            'nom': nom,
            'timestamp': datetime.now().isoformat(),
            'sequence_originale': sequence,
            'pyramide': pyramide,
            'signatures': signatures,
            'interpretation': interpretation,
            'preuves_integrite': self._generer_preuves(pyramide)
        }
        
        # Archivage
        self.archives_analyses[nom] = resultat
        self.historique_operations.append({
            'action': 'ANALYSE',
            'nom': nom,
            'timestamp': resultat['timestamp'],
            'signature_racine': signatures['signature_racine']
        })
        
        return resultat
    
    def _construire_pyramide(self, sequence: List[int]) -> Dict[str, List[List[int]]]:
        """Construit la pyramide complète avec parties supérieure et inférieure"""
        
        pyramide = {
            'base': sequence,
            'superieure': [],
            'inferieure': []
        }
        
        # Construction partie supérieure (additions)
        current = sequence.copy()
        while len(current) > 1:
            next_level = [current[i] + current[i+1] for i in range(len(current)-1)]
            pyramide['superieure'].insert(0, next_level)
            current = next_level
        
        # Construction partie inférieure (différences absolues)
        current = sequence.copy()
        while len(current) > 1:
            next_level = [abs(current[i] - current[i+1]) for i in range(len(current)-1)]
            pyramide['inferieure'].append(next_level)
            current = next_level
        
        return pyramide
    
    def _calculer_signatures(self, pyramide: Dict, nom: str) -> Dict:
        """Calcule les signatures uniques de la pyramide"""
        
        sommet = pyramide['superieure'][0][0] if pyramide['superieure'] else pyramide['base'][0]
        base = pyramide['inferieure'][-1][0] if pyramide['inferieure'] else pyramide['base'][0]
        
        # Signature cryptographique
        data_crypto = nom + ''.join(str(x) for niveau in pyramide['superieure'] for x in niveau)
        hash_verite = hashlib.sha256(data_crypto.encode()).hexdigest()
        
        # Signature de convergence
        convergence_data = f"{sommet}:{base}:{pyramide['base'][0]}:{pyramide['base'][-1]}"
        hash_convergence = hashlib.sha256(convergence_data.encode()).hexdigest()[:16]
        
        return {
            'signature_racine': f"VERITE-{hash_verite[:16]}",
            'sommet_pyramidal': sommet,
            'base_fondamentale': base,
            'hash_convergence': hash_convergence,
            'niveaux_total': len(pyramide['superieure']) + len(pyramide['inferieure']) + 1,
            'symetrie_score': self._calculer_symetrie(pyramide),
            'ratio_harmonie': self._calculer_ratio_harmonie(sommet, base)
        }
    
    def _calculer_symetrie(self, pyramide: Dict) -> float:
        """Calcule le score de symétrie de la pyramide"""
        if not pyramide['superieure'] or not pyramide['inferieure']:
            return 0.0
        
        niveaux_sup = len(pyramide['superieure'])
        niveaux_inf = len(pyramide['inferieure'])
        
        if niveaux_sup == 0 or niveaux_inf == 0:
            return 0.0
        
        return 1.0 - (abs(niveaux_sup - niveaux_inf) / max(niveaux_sup, niveaux_inf))
    
    def _calculer_ratio_harmonie(self, sommet: int, base: int) -> float:
        """Calcule le ratio d'harmonie entre sommet et base"""
        if base == 0:
            return 0.0
        
        ratio = min(sommet, base) / max(sommet, base)
        # Plus proche du nombre d'or (0.618), meilleure l'harmonie
        return 1.0 - abs(ratio - 0.618)
    
    def _interpreter_pyramide(self, pyramide: Dict, nom: str) -> Dict:
        """Interprète la signification structurelle de la pyramide"""
        
        sommet = pyramide['superieure'][0][0] if pyramide['superieure'] else pyramide['base'][0]
        base = pyramide['inferieure'][-1][0] if pyramide['inferieure'] else pyramide['base'][0]
        
        # Analyse des patterns
        patterns = {
            'unite_fondamentale': base == 1,
            'equilibre_parfait': sommet == base,
            'croissance_harmonieuse': len(pyramide['superieure']) == len(pyramide['inferieure']),
            'convergence_rapide': len(pyramide['inferieure']) < 4,
            'stabilite_structurelle': self._evaluer_stabilite(pyramide)
        }
        
        # Principes structurels
        principes = []
        
        if patterns['unite_fondamentale']:
            principes.append("Unité fondamentale - convergence vers l'essentiel")
        
        if patterns['equilibre_parfait']:
            principes.append("Équilibre parfait entre complexité et simplicité")
        
        if patterns['croissance_harmonieuse']:
            principes.append("Croissance et réduction harmonieuses")
        else:
            principes.append("Dynamique asymétrique entre construction et déconstruction")
        
        if patterns['convergence_rapide']:
            principes.append("Convergence rapide vers la stabilité")
        else:
            principes.append("Convergence progressive nécessitant une exploration approfondie")
        
        if patterns['stabilite_structurelle']:
            principes.append("Structure stable et cohérente")
        else:
            principes.append("Structure dynamique en évolution")
        
        return {
            'principes_structurels': principes,
            'patterns_detectes': patterns,
            'message_essentiel': self._generer_message_essentiel(nom, sommet, base),
            'niveau_complexite': self._evaluer_complexite(pyramide),
            'score_harmonie': self._calculer_score_harmonie_global(pyramide)
        }
    
    def _evaluer_stabilite(self, pyramide: Dict) -> bool:
        """Évalue la stabilité structurelle de la pyramide"""
        if not pyramide['inferieure']:
            return True
        
        base_finale = pyramide['inferieure'][-1]
        # Stabilité si la base finale a peu de variations
        if len(base_finale) == 1:
            return True
        
        ecart_type = np.std(base_finale)
        return ecart_type < 10  # Seuil arbitraire
    
    def _generer_message_essentiel(self, nom: str, sommet: int, base: int) -> str:
        """Génère le message structurel essentiel"""
        
        messages = {
            (1, 1): f"« {nom} » incarne l'unité parfaite - essence pure et stable",
            (0, 0): f"« {nom} » représente le potentiel infini - vide créateur",
            (2, 2): f"« {nom} » symbolise la dualité équilibrée - complémentarité parfaite"
        }
        
        # Message basé sur le ratio
        ratio = min(sommet, base) / max(sommet, base) if max(sommet, base) > 0 else 0
        
        if ratio > 0.9:
            message = f"« {nom} » : Équilibre remarquable ({sommet} ↔ {base})"
        elif ratio > 0.7:
            message = f"« {nom} » : Harmonisation avancée ({sommet} → {base})"
        elif ratio > 0.5:
            message = f"« {nom} » : Transition équilibrée ({sommet} → {base})"
        else:
            message = f"« {nom} » : Transformation profonde ({sommet} → {base})"
        
        return messages.get((sommet, base), message)
    
    def _evaluer_complexite(self, pyramide: Dict) -> ComplexiteNiveau:
        """Évalue le niveau de complexité structurelle"""
        total_niveaux = len(pyramide['superieure']) + len(pyramide['inferieure'])
        
        if total_niveaux <= 3:
            return ComplexiteNiveau.SIMPLE
        elif total_niveaux <= 6:
            return ComplexiteNiveau.MODEREE
        elif total_niveaux <= 9:
            return ComplexiteNiveau.COMPLEXE
        else:
            return ComplexiteNiveau.TRES_COMPLEXE
    
    def _calculer_score_harmonie_global(self, pyramide: Dict) -> float:
        """Calcule un score d'harmonie global"""
        scores = []
        
        # Symétrie structurelle
        scores.append(self._calculer_symetrie(pyramide))
        
        # Stabilité
        scores.append(1.0 if self._evaluer_stabilite(pyramide) else 0.5)
        
        # Équilibre des valeurs
        if pyramide['superieure'] and pyramide['inferieure']:
            valeurs_sup = [item for niveau in pyramide['superieure'] for item in niveau]
            valeurs_inf = [item for niveau in pyramide['inferieure'] for item in niveau]
            
            if valeurs_sup and valeurs_inf:
                avg_sup = np.mean(valeurs_sup)
                avg_inf = np.mean(valeurs_inf)
                if max(avg_sup, avg_inf) > 0:
                    equilibre = 1.0 - (abs(avg_sup - avg_inf) / max(avg_sup, avg_inf))
                    scores.append(equilibre)
        
        return np.mean(scores) if scores else 0.5
    
    def _generer_preuves(self, pyramide: Dict) -> Dict:
        """Génère les preuves d'intégrité de la pyramide"""
        
        # Preuve de cohérence mathématique
        somme_sup = sum(item for niveau in pyramide['superieure'] for item in niveau)
        somme_inf = sum(item for niveau in pyramide['inferieure'] for item in niveau)
        
        # Preuve de convergence
        convergence_point = pyramide['inferieure'][-1][0] if pyramide['inferieure'] else pyramide['base'][0]
        
        return {
            'preuve_coherence': somme_sup + somme_inf,
            'preuve_convergence': convergence_point,
            'preuve_authenticite': hashlib.sha256(
                str(somme_sup + somme_inf + convergence_point).encode()
            ).hexdigest()[:12],
            'timestamp_verification': datetime.now().isoformat()
        }
    
    def verifier_integrite(self, nom: str) -> Dict:
        """Vérifie l'intégrité d'une analyse précédente"""
        
        if nom not in self.archives_analyses:
            return {'statut': 'NON_TROUVE', 'message': 'Aucune analyse existante'}
        
        analyse_originale = self.archives_analyses[nom]
        nouvelle_analyse = self.analyser_sequence(analyse_originale['sequence_originale'], nom)
        
        # Comparaison des signatures
        integrite = (
            analyse_originale['signatures']['signature_racine'] == 
            nouvelle_analyse['signatures']['signature_racine']
        )
        
        resultat = {
            'statut': 'INTÈGRE' if integrite else 'CORROMPU',
            'nom': nom,
            'timestamp_verification': datetime.now().isoformat(),
            'signature_originale': analyse_originale['signatures']['signature_racine'],
            'signature_actuelle': nouvelle_analyse['signatures']['signature_racine'],
            'confiance': 1.0 if integrite else 0.0
        }
        
        self.historique_operations.append({
            'action': 'VERIFICATION',
            'nom': nom,
            'statut': resultat['statut'],
            'timestamp': resultat['timestamp_verification']
        })
        
        return resultat
    
    def comparer_sequences(self, seq1: List[int], nom1: str, seq2: List[int], nom2: str) -> Dict:
        """Compare la structure pyramidale de deux séquences"""
        
        analyse1 = self.analyser_sequence(seq1, nom1)
        analyse2 = self.analyser_sequence(seq2, nom2)
        
        similarite = self._calculer_similarite_pyramidale(
            analyse1['pyramide'], 
            analyse2['pyramide']
        )
        
        return {
            'sequences_comparées': [nom1, nom2],
            'score_similarite': similarite,
            'relation': self._determiner_relation(similarite),
            'differences_structurelles': self._analyser_differences(
                analyse1['pyramide'], 
                analyse2['pyramide']
            ),
            'timestamp_comparaison': datetime.now().isoformat()
        }
    
    def _calculer_similarite_pyramidale(self, pyramide1: Dict, pyramide2: Dict) -> float:
        """Calcule le score de similarité entre deux pyramides"""
        
        # Similarité des bases
        base1 = pyramide1['base']
        base2 = pyramide2['base']
        
        if len(base1) != len(base2):
            similarite_base = 0.3
        else:
            differences = sum(abs(a - b) for a, b in zip(base1, base2))
            max_diff = max(max(base1), max(base2)) * len(base1) if base1 and base2 else 1
            similarite_base = 1.0 - (differences / max_diff if max_diff > 0 else 0)
        
        # Similarité structurelle
        structure_sim = 1.0 - (
            abs(len(pyramide1['superieure']) - len(pyramide2['superieure'])) / 
            max(len(pyramide1['superieure']), len(pyramide2['superieure']), 1)
        )
        
        return (similarite_base + structure_sim) / 2
    
    def _determiner_relation(self, similarite: float) -> str:
        """Détermine la relation entre deux séquences basée sur la similarité"""
        if similarite >= 0.9:
            return "IDENTITÉ STRUCTURELLE"
        elif similarite >= 0.7:
            return "FORTE AFFINITÉ"
        elif similarite >= 0.5:
            return "RELATION MODÉRÉE"
        elif similarite >= 0.3:
            return "FAIBLE CONNEXION"
        else:
            return "DISSIMILARITÉ"
    
    def _analyser_differences(self, pyramide1: Dict, pyramide2: Dict) -> List[str]:
        """Analyse les différences structurelles entre deux pyramides"""
        differences = []
        
        if len(pyramide1['base']) != len(pyramide2['base']):
            differences.append("Longueur de base différente")
        
        if len(pyramide1['superieure']) != len(pyramide2['superieure']):
            differences.append("Hauteur pyramidale supérieure différente")
        
        if len(pyramide1['inferieure']) != len(pyramide2['inferieure']):
            differences.append("Profondeur pyramidale inférieure différente")
        
        # Différence de convergence
        conv1 = pyramide1['inferieure'][-1][0] if pyramide1['inferieure'] else pyramide1['base'][0]
        conv2 = pyramide2['inferieure'][-1][0] if pyramide2['inferieure'] else pyramide2['base'][0]
        
        if conv1 != conv2:
            differences.append(f"Points de convergence différents ({conv1} vs {conv2})")
        
        return differences
    
    def generer_rapport(self, sequence: List[int], nom: str) -> str:
        """Génère un rapport complet d'analyse"""
        
        analyse = self.analyser_sequence(sequence, nom)
        
        rapport = f"""
╔═══════════════════════════════════════╗
║         RAPPORT ALGO VÉRITÉ          ║
║           Analyse Pyramidale          ║
╚═══════════════════════════════════════╝

NOM : {analyse['nom']}
TIMESTAMP : {analyse['timestamp']}

SÉQUENCE ORIGINALE
──────────────────
{analyse['sequence_originale']}

STRUCTURE PYRAMIDALE
────────────────────
• Niveaux supérieurs : {len(analyse['pyramide']['superieure'])}
• Niveaux inférieurs : {len(analyse['pyramide']['inferieure'])}
• Base : {analyse['pyramide']['base']}

SIGNATURES UNIQUES
──────────────────
• Racine : {analyse['signatures']['signature_racine']}
• Sommet : {analyse['signatures']['sommet_pyramidal']}
• Base : {analyse['signatures']['base_fondamentale']}
• Score symétrie : {analyse['signatures']['symetrie_score']:.2f}
• Ratio harmonie : {analyse['signatures']['ratio_harmonie']:.2f}

INTERPRÉTATION STRUCTURELLE
───────────────────────────
• Message essentiel : {analyse['interpretation']['message_essentiel']}
• Complexité : {analyse['interpretation']['niveau_complexite'].value}
• Score harmonie : {analyse['interpretation']['score_harmonie']:.2f}

PRINCIPES DÉTECTÉS
──────────────────
"""
        for principe in analyse['interpretation']['principes_structurels']:
            rapport += f"• {principe}\n"
        
        rapport += f"""
PREUVES D'INTÉGRITÉ
───────────────────
• Cohérence : {analyse['preuves_integrite']['preuve_coherence']}
• Convergence : {analyse['preuves_integrite']['preuve_convergence']}
• Authenticité : {analyse['preuves_integrite']['preuve_authenticite']}

════════════════════════════════════════
         FIN DU RAPPORT VÉRITÉ
════════════════════════════════════════
"""
        return rapport