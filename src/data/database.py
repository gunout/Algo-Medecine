import sqlite3
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Gestionnaire de base de données pour Algo Vérité Médical
    """
    
    def __init__(self, db_path: str = "algo_verite_medical.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialise la structure de la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Table des patients
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS patients (
                        id TEXT PRIMARY KEY,
                        data JSON NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Table des analyses
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS analyses (
                        id TEXT PRIMARY KEY,
                        patient_id TEXT,
                        analysis_data JSON NOT NULL,
                        pyramid_structure JSON NOT NULL,
                        predictions JSON NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id)
                    )
                ''')
                
                # Table des traitements
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS treatments (
                        id TEXT PRIMARY KEY,
                        patient_id TEXT,
                        treatment_data JSON NOT NULL,
                        effectiveness_score REAL,
                        status TEXT DEFAULT 'recommended',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id)
                    )
                ''')
                
                # Table de suivi
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS follow_ups (
                        id TEXT PRIMARY KEY,
                        patient_id TEXT,
                        day_number INTEGER,
                        health_status TEXT,
                        symptoms JSON,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id)
                    )
                ''')
                
                conn.commit()
                logger.info("Base de données initialisée avec succès")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def save_patient(self, patient_data: Dict[str, Any]) -> str:
        """Sauvegarde un patient dans la base de données"""
        try:
            patient_id = patient_data.get('id', f"PAT_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO patients (id, data, updated_at)
                    VALUES (?, ?, ?)
                ''', (patient_id, json.dumps(patient_data), datetime.now().isoformat()))
                
                conn.commit()
                logger.info(f"Patient sauvegardé: {patient_id}")
                return patient_id
                
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du patient: {e}")
            raise
    
    def save_analysis(self, patient_id: str, analysis_data: Dict[str, Any]) -> str:
        """Sauvegarde une analyse médicale"""
        try:
            analysis_id = f"ANA_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO analyses (id, patient_id, analysis_data, pyramid_structure, predictions)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    analysis_id,
                    patient_id,
                    json.dumps(analysis_data),
                    json.dumps(analysis_data.get('pyramide_sante', {})),
                    json.dumps(analysis_data.get('prediction_retablissement', {}))
                ))
                
                conn.commit()
                logger.info(f"Analyse sauvegardée: {analysis_id} pour patient: {patient_id}")
                return analysis_id
                
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'analyse: {e}")
            raise
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un patient par son ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row['id'],
                        'data': json.loads(row['data']),
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du patient: {e}")
            return None
    
    def get_patient_analyses(self, patient_id: str) -> List[Dict[str, Any]]:
        """Récupère toutes les analyses d'un patient"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM analyses WHERE patient_id = ? ORDER BY created_at DESC', (patient_id,))
                rows = cursor.fetchall()
                
                analyses = []
                for row in rows:
                    analyses.append({
                        'id': row['id'],
                        'patient_id': row['patient_id'],
                        'analysis_data': json.loads(row['analysis_data']),
                        'pyramid_structure': json.loads(row['pyramid_structure']),
                        'predictions': json.loads(row['predictions']),
                        'created_at': row['created_at']
                    })
                
                return analyses
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des analyses: {e}")
            return []
    
    def get_all_patients(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupère tous les patients"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM patients ORDER BY updated_at DESC LIMIT ?', (limit,))
                rows = cursor.fetchall()
                
                patients = []
                for row in rows:
                    patients.append({
                        'id': row['id'],
                        'data': json.loads(row['data']),
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    })
                
                return patients
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des patients: {e}")
            return []
    
    def add_follow_up(self, patient_id: str, day_number: int, health_status: str, symptoms: List[str], notes: str = ""):
        """Ajoute une entrée de suivi"""
        try:
            follow_up_id = f"FU_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO follow_ups (id, patient_id, day_number, health_status, symptoms, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (follow_up_id, patient_id, day_number, health_status, json.dumps(symptoms), notes))
                
                conn.commit()
                logger.info(f"Suivi ajouté: {follow_up_id} pour patient: {patient_id}")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du suivi: {e}")
            raise
    
    def get_patient_follow_ups(self, patient_id: str) -> List[Dict[str, Any]]:
        """Récupère le suivi d'un patient"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    'SELECT * FROM follow_ups WHERE patient_id = ? ORDER BY day_number ASC', 
                    (patient_id,)
                )
                rows = cursor.fetchall()
                
                follow_ups = []
                for row in rows:
                    follow_ups.append({
                        'id': row['id'],
                        'patient_id': row['patient_id'],
                        'day_number': row['day_number'],
                        'health_status': row['health_status'],
                        'symptoms': json.loads(row['symptoms']),
                        'notes': row['notes'],
                        'created_at': row['created_at']
                    })
                
                return follow_ups
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du suivi: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Récupère des statistiques globales"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Nombre total de patients
                cursor = conn.execute('SELECT COUNT(*) as total FROM patients')
                total_patients = cursor.fetchone()[0]
                
                # Nombre total d'analyses
                cursor = conn.execute('SELECT COUNT(*) as total FROM analyses')
                total_analyses = cursor.fetchone()[0]
                
                # Pathologies les plus courantes
                cursor = conn.execute('''
                    SELECT data->>'$.pathologie' as pathology, COUNT(*) as count 
                    FROM patients 
                    GROUP BY pathology 
                    ORDER BY count DESC 
                    LIMIT 5
                ''')
                common_pathologies = [{'pathology': row[0], 'count': row[1]} for row in cursor.fetchall()]
                
                # Dernières analyses
                cursor = conn.execute('''
                    SELECT a.created_at, p.data->>'$.pathologie' as pathology 
                    FROM analyses a 
                    JOIN patients p ON a.patient_id = p.id 
                    ORDER BY a.created_at DESC 
                    LIMIT 5
                ''')
                recent_analyses = [{'date': row[0], 'pathology': row[1]} for row in cursor.fetchall()]
                
                return {
                    'total_patients': total_patients,
                    'total_analyses': total_analyses,
                    'common_pathologies': common_pathologies,
                    'recent_analyses': recent_analyses,
                    'database_size': f"{self._get_database_size()} MB"
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {}
    
    def _get_database_size(self) -> float:
        """Retourne la taille de la base de données en MB"""
        import os
        if os.path.exists(self.db_path):
            return round(os.path.getsize(self.db_path) / (1024 * 1024), 2)
        return 0.0
    
    def export_data(self, export_path: str):
        """Exporte les données vers un fichier JSON"""
        try:
            data = {
                'export_date': datetime.now().isoformat(),
                'patients': self.get_all_patients(limit=1000),
                'statistics': self.get_statistics()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Données exportées vers: {export_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export des données: {e}")
            raise
    
    def cleanup_old_data(self, days_old: int = 30):
        """Nettoie les anciennes données"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            
            with sqlite3.connect(self.db_path) as conn:
                # Supprimer les suivis anciens
                conn.execute('DELETE FROM follow_ups WHERE created_at < ?', (cutoff_date,))
                
                # Supprimer les analyses sans patients associés
                conn.execute('DELETE FROM analyses WHERE patient_id NOT IN (SELECT id FROM patients)')
                
                conn.commit()
                logger.info(f"Données de plus de {days_old} jours nettoyées")
                
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage des données: {e}")