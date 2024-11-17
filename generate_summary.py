import google.generativeai as genai
import json
def generate_summary(terms: str, model_type: str = 'models/gemini-1.5-flash-001') -> str:
    # Barème détaillé des critères
    try:
        grading_criteria = """
    ### 1. Clarté et Accessibilité (10 points)
    - **Langage clair et compréhensible (5 points) :** Les documents sont-ils rédigés sans jargon juridique excessif et sont-ils faciles à comprendre pour un utilisateur moyen ?
    - **Facilité d'accès (5 points) :** Les CGU et la Politique de Confidentialité sont-elles facilement accessibles depuis toutes les pages du site ?

    ### 2. Transparence sur la Collecte et l'Utilisation des Données (15 points)
    - **Données collectées (5 points) :** Le site spécifie-t-il quelles données personnelles sont collectées ?
    - **Méthodes de collecte (5 points) :** Les moyens par lesquels les données sont collectées sont-ils clairement expliqués (cookies, formulaires, etc.) ?
    - **Utilisation des données (5 points) :** Les finalités pour lesquelles les données sont utilisées sont-elles clairement décrites ?

    ### 3. Droits et Contrôle de l'Utilisateur (10 points)
    - **Accès et rectification (5 points) :** Les utilisateurs sont-ils informés de leur droit d'accéder à leurs données et de les corriger ?
    - **Suppression et opposition (5 points) :** Le droit à l'oubli et le droit de s'opposer au traitement des données sont-ils mentionnés ?

    ### 4. Partage des Données avec des Tiers (10 points)
    - **Divulgation à des tiers (5 points) :** Le site indique-t-il si les données sont partagées avec des partenaires ou des tiers ?
    - **Finalités du partage (5 points) :** Les raisons du partage de données sont-elles clairement justifiées ?

    ### 5. Mesures de Sécurité (5 points)
    - **Protection des données (5 points) :** Le site décrit-il les mesures prises pour assurer la sécurité des données personnelles ?

    ### 6. Conformité aux Lois et Réglementations (10 points)
    - **Respect des réglementations (5 points) :** Les documents font-ils référence aux lois applicables (RGPD, CCPA, etc.) ?
    - **Délégué à la protection des données (5 points) :** Un contact pour le délégué à la protection des données est-il fourni ?

    ### 7. Équité des Conditions Générales d'Utilisation (10 points)
    - **Clauses équilibrées (5 points) :** Les CGU contiennent-elles des clauses abusives ou déséquilibrées en défaveur de l'utilisateur ?
    - **Responsabilités clairement définies (5 points) :** Les responsabilités du site et de l'utilisateur sont-elles clairement établies ?

    ### 8. Résolution des Litiges et Juridiction (5 points)
    - **Procédure de litige (3 points) :** La procédure en cas de litige est-elle clairement expliquée ?
    - **Loi applicable et juridiction (2 points) :** La juridiction compétente est-elle mentionnée de manière équitable pour l'utilisateur ?

    ### 9. Mises à Jour et Notifications (5 points)
    - **Notification des changements (3 points) :** Le site informe-t-il les utilisateurs des modifications apportées aux documents ?
    - **Acceptation des nouvelles conditions (2 points) :** Le processus d'acceptation des mises à jour est-il décrit ?

    ### 10. Utilisation de Cookies et Technologies de Suivi (5 points)
    - **Informations sur les cookies (3 points) :** Le site explique-t-il l'utilisation des cookies et autres traceurs ?
    - **Gestion des préférences (2 points) :** Les utilisateurs peuvent-ils personnaliser leurs paramètres de cookies ?

    ### 11. Mécanismes de Consentement (5 points)
    - **Obtention du consentement (3 points) :** Le consentement est-il obtenu avant la collecte des données ?
    - **Retrait du consentement (2 points) :** Les utilisateurs peuvent-ils facilement retirer leur consentement ?

    ### 12. Pratiques Douteuses dans le Domaine d'Activité (15 points)
    - **Transparence sur les pratiques spécifiques (10 points) :** Le site divulgue-t-il clairement les pratiques spécifiques à son secteur, surtout si elles peuvent être controversées ?
    - **Éthique et conformité (5 points) :** Le site adhère-t-il à des normes éthiques reconnues dans son domaine ?
    """

        # Construction du prompt
        prompt = f"""
    Veuillez analyser les Conditions Générales d'Utilisation (CGU) et la Politique de Confidentialité suivantes :

    {terms}

    Basé sur les documents fournis, veuillez :

    1. Évaluer chacun des critères suivants et attribuer un score selon le barème (totalisant 100 points) :

    {grading_criteria}

    Fournissez les scores pour chaque catégorie.

    2. Créer un fichier JSON qui inclut :

    - Les scores pour chaque domaine.
    - Une liste des données collectées par le site.
    - Indiquez si ces données sont partagées avec des tiers.
    - Un paragraphe détaillant tous les frais du site.
    - Des informations sur la possibilité de résilier un abonnement, et comment.
    - Un paragraphe sur la manière de contacter le support.

    Le JSON doit être structuré comme suit :

    {{
    "scores": {{
        "clarity_and_accessibility": 10,
        "transparency_on_data_collection_and_use": 15,
        "user_rights_and_control": 10,
        "data_sharing_with_third_parties": 10,
        "security_measures": 5,
        "legal_compliance": 10,
        "fairness_of_terms": 10,
        "dispute_resolution_and_jurisdiction": 5,
        "updates_and_notifications": 5,
        "cookies_and_tracking": 5,
        "consent_mechanisms": 5,
        "industry_specific_practices": 15
    }},
    "data_collected": ["email", "nom", "données d'utilisation", ...],
    "data_shared": true,
    "fees": "Détails sur tous les frais du site",
    "subscription_cancellation": "Informations sur la façon de résilier un abonnement",
    "support_contact": "Informations sur la manière de contacter le support"
    }}

    3. N'incluez aucun commentaire ou texte supplémentaire en dehors du JSON.
    """


        genai.configure(api_key="AIzaSyB-lGipmE-uSN0pr-2XZ6OP8ApI-YEPU3o")
            
        model_gemini = genai.GenerativeModel(model_type)
        response = model_gemini.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=1500,
                temperature=0
            ),
            stream=False
        )

        # Extract the JSON string from the response
        generated_json = response.candidates[0]['content']  # Assuming the response is structured this way.

        # Validate and clean the JSON string
        parsed_json = json.loads(generated_json)  # Ensure the string is valid JSON.

        # Return the JSON as a string for JavaScript
        return json.dumps(parsed_json)  # Convert back to a JSON-formatted string.

    except Exception as e:

        return f"Error generating summary: {str(e)}"
