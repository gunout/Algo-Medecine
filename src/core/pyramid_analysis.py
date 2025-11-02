import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class PyramidType(Enum):
    PERFECT = "PYRAMIDE_PARFAITE"
    STABLE = "PYRAMIDE_STABLE"
    UNSTABLE = "PYRAMIDE_INSTABLE"
    HARMONIOUS = "PYRAMIDE_HARMONIEUSE"
    CHAOTIC = "PYRAMIDE_CHAOTIQUE"

@dataclass
class PyramidMetrics:
    height: int
    width: int
    stability_score: float
    symmetry_score: float
    convergence_speed: float
    entropy: float

class PyramidAnalyzer:
    """
    Analyse spécialisée des structures pyramidales
    """
    
    def __init__(self):
        self.analysis_cache = {}
    
    def analyze_pyramid_structure(self, base_sequence: List[int]) -> Dict[str, Any]:
        """Analyse approfondie de la structure pyramidale"""
        
        # Construction de la pyramide
        pyramid = self._build_pyramid(base_sequence)
        
        # Calcul des métriques
        metrics = self._calculate_pyramid_metrics(pyramid)
        
        # Classification
        pyramid_type = self._classify_pyramid(metrics)
        
        # Patterns détectés
        patterns = self._detect_patterns(pyramid, metrics)
        
        return {
            'pyramid': pyramid,
            'metrics': metrics.__dict__,
            'type': pyramid_type.value,
            'patterns': patterns,
            'recommendations': self._generate_recommendations(metrics, pyramid_type)
        }
    
    def _build_pyramid(self, base: List[int]) -> Dict[str, List[List[int]]]:
        """Construit la pyramide complète"""
        pyramid = {
            'base': base,
            'upper': [],
            'lower': []
        }
        
        # Partie supérieure
        current = base.copy()
        while len(current) > 1:
            next_level = [current[i] + current[i+1] for i in range(len(current)-1)]
            pyramid['upper'].insert(0, next_level)
            current = next_level
        
        # Partie inférieure
        current = base.copy()
        while len(current) > 1:
            next_level = [abs(current[i] - current[i+1]) for i in range(len(current)-1)]
            pyramid['lower'].append(next_level)
            current = next_level
        
        return pyramid
    
    def _calculate_pyramid_metrics(self, pyramid: Dict) -> PyramidMetrics:
        """Calcule les métriques de la pyramide"""
        
        base_len = len(pyramid['base'])
        upper_height = len(pyramid['upper'])
        lower_height = len(pyramid['lower'])
        
        # Score de stabilité
        stability = self._calculate_stability(pyramid)
        
        # Score de symétrie
        symmetry = 1.0 - (abs(upper_height - lower_height) / max(upper_height, lower_height, 1))
        
        # Vitesse de convergence
        convergence = lower_height / base_len if base_len > 0 else 0
        
        # Entropie de la base
        entropy = self._calculate_entropy(pyramid['base'])
        
        return PyramidMetrics(
            height=max(upper_height, lower_height),
            width=base_len,
            stability_score=stability,
            symmetry_score=symmetry,
            convergence_speed=convergence,
            entropy=entropy
        )
    
    def _calculate_stability(self, pyramid: Dict) -> float:
        """Calcule le score de stabilité"""
        if not pyramid['lower']:
            return 1.0
        
        final_level = pyramid['lower'][-1]
        if len(final_level) == 1:
            return 1.0
        
        # Moins de variation = plus stable
        variation = np.std(final_level) / (np.mean(final_level) if np.mean(final_level) != 0 else 1)
        return max(0, 1 - variation)
    
    def _calculate_entropy(self, sequence: List[int]) -> float:
        """Calcule l'entropie de la séquence"""
        if not sequence:
            return 0
        
        # Normalisation
        seq_array = np.array(sequence)
        if np.sum(seq_array) == 0:
            return 0
        
        probabilities = seq_array / np.sum(seq_array)
        probabilities = probabilities[probabilities > 0]  # Éviter log(0)
        
        return float(-np.sum(probabilities * np.log(probabilities)))
    
    def _classify_pyramid(self, metrics: PyramidMetrics) -> PyramidType:
        """Classifie le type de pyramide"""
        
        if metrics.symmetry_score > 0.9 and metrics.stability_score > 0.9:
            return PyramidType.PERFECT
        elif metrics.stability_score > 0.7:
            return PyramidType.STABLE
        elif metrics.symmetry_score > 0.8:
            return PyramidType.HARMONIOUS
        elif metrics.stability_score < 0.3:
            return PyramidType.UNSTABLE
        else:
            return PyramidType.CHAOTIC
    
    def _detect_patterns(self, pyramid: Dict, metrics: PyramidMetrics) -> List[str]:
        """Détecte les patterns dans la pyramide"""
        patterns = []
        
        # Pattern de Fibonacci
        if self._is_fibonacci_like(pyramid['base']):
            patterns.append("Séquence de type Fibonacci")
        
        # Pattern géométrique
        if self._is_geometric_sequence(pyramid['base']):
            patterns.append("Progression géométrique")
        
        # Pattern arithmétique
        if self._is_arithmetic_sequence(pyramid['base']):
            patterns.append("Progression arithmétique")
        
        # Pattern de convergence rapide
        if metrics.convergence_speed > 0.7:
            patterns.append("Convergence rapide")
        
        # Pattern d'harmonie
        if metrics.symmetry_score > 0.8:
            patterns.append("Structure harmonieuse")
        
        return patterns
    
    def _is_fibonacci_like(self, sequence: List[int]) -> bool:
        """Vérifie si la séquence ressemble à Fibonacci"""
        if len(sequence) < 3:
            return False
        
        for i in range(2, len(sequence)):
            if sequence[i] != sequence[i-1] + sequence[i-2]:
                return False
        return True
    
    def _is_geometric_sequence(self, sequence: List[int]) -> bool:
        """Vérifie si c'est une suite géométrique"""
        if len(sequence) < 2:
            return False
        
        ratios = []
        for i in range(1, len(sequence)):
            if sequence[i-1] == 0:
                return False
            ratios.append(sequence[i] / sequence[i-1])
        
        return np.std(ratios) < 0.1  # Faible variation des ratios
    
    def _is_arithmetic_sequence(self, sequence: List[int]) -> bool:
        """Vérifie si c'est une suite arithmétique"""
        if len(sequence) < 2:
            return False
        
        differences = [sequence[i] - sequence[i-1] for i in range(1, len(sequence))]
        return np.std(differences) < 0.1  # Faible variation des différences
    
    def _generate_recommendations(self, metrics: PyramidMetrics, pyramid_type: PyramidType) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []
        
        if pyramid_type == PyramidType.UNSTABLE:
            recommendations.append("Structure instable - recommandation: renforcer la cohérence")
        
        if metrics.symmetry_score < 0.6:
            recommendations.append("Asymétrie détectée - équilibrer construction/déconstruction")
        
        if metrics.convergence_speed < 0.3:
            recommendations.append("Convergence lente - simplifier la structure de base")
        
        if metrics.entropy > 2.0:
            recommendations.append("Entropie élevée - réduire la complexité aléatoire")
        
        if not recommendations:
            recommendations.append("Structure optimale - maintenir la configuration actuelle")
        
        return recommendations
    
    def compare_pyramids(self, pyramid1: Dict, pyramid2: Dict) -> Dict[str, Any]:
        """Compare deux pyramides"""
        metrics1 = self._calculate_pyramid_metrics(pyramid1)
        metrics2 = self._calculate_pyramid_metrics(pyramid2)
        
        similarity_score = self._calculate_pyramid_similarity(metrics1, metrics2)
        
        return {
            'similarity_score': similarity_score,
            'metrics_differences': self._compare_metrics(metrics1, metrics2),
            'compatibility': self._assess_compatibility(metrics1, metrics2)
        }
    
    def _calculate_pyramid_similarity(self, metrics1: PyramidMetrics, metrics2: PyramidMetrics) -> float:
        """Calcule la similarité entre deux pyramides"""
        similarities = []
        
        # Similarité de hauteur
        height_sim = 1 - abs(metrics1.height - metrics2.height) / max(metrics1.height, metrics2.height, 1)
        similarities.append(height_sim)
        
        # Similarité de stabilité
        stability_sim = 1 - abs(metrics1.stability_score - metrics2.stability_score)
        similarities.append(stability_sim)
        
        # Similarité de symétrie
        symmetry_sim = 1 - abs(metrics1.symmetry_score - metrics2.symmetry_score)
        similarities.append(symmetry_sim)
        
        return np.mean(similarities)
    
    def _compare_metrics(self, metrics1: PyramidMetrics, metrics2: PyramidMetrics) -> Dict[str, float]:
        """Compare les métriques individuelles"""
        return {
            'height_difference': abs(metrics1.height - metrics2.height),
            'stability_difference': abs(metrics1.stability_score - metrics2.stability_score),
            'symmetry_difference': abs(metrics1.symmetry_score - metrics2.symmetry_score),
            'convergence_difference': abs(metrics1.convergence_speed - metrics2.convergence_speed)
        }
    
    def _assess_compatibility(self, metrics1: PyramidMetrics, metrics2: PyramidMetrics) -> str:
        """Évalue la compatibilité entre deux pyramides"""
        similarity = self._calculate_pyramid_similarity(metrics1, metrics2)
        
        if similarity > 0.9:
            return "COMPATIBILITÉ PARFAITE"
        elif similarity > 0.7:
            return "HAUTE COMPATIBILITÉ"
        elif similarity > 0.5:
            return "COMPATIBILITÉ MODÉRÉE"
        else:
            return "FAIBLE COMPATIBILITÉ"