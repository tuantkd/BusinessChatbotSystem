import pandas as pd

def write_result_data_to_excel(result_data, test_id):
    # Process intent_evaluation
    if 'intent_evaluation' in result_data:
        intent_eval = result_data['intent_evaluation']
        intent_eval_file = f'static/results/intent_evaluation_{test_id}.xlsx'
        
        with pd.ExcelWriter(intent_eval_file, engine='openpyxl') as writer:
            # Predictions sheet
            if 'predictions' in intent_eval:
                predictions_df = pd.DataFrame(intent_eval['predictions'])
                predictions_df.to_excel(writer, sheet_name='predictions', index=False)
            
            # Errors sheet
            if 'errors' in intent_eval:
                errors_df = pd.DataFrame(intent_eval['errors'])
                errors_df.to_excel(writer, sheet_name='errors', index=False)
    
    # Process entity_evaluation
    if 'entity_evaluation' in result_data:
        entity_eval = result_data['entity_evaluation']
        entity_eval_file = f'static/results/entity_evaluation_{test_id}.xlsx'
        
        with pd.ExcelWriter(entity_eval_file, engine='openpyxl') as writer:
            # DIETClassifier sheet
            if 'DIETClassifier' in entity_eval:
                diet_classifier_df = pd.DataFrame(entity_eval['DIETClassifier'])
                diet_classifier_df.to_excel(writer, sheet_name='DIETClassifier', index=False)
    
    return intent_eval_file, entity_eval_file
