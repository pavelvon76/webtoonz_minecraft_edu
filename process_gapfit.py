import json
import csv

# Read current gapfit.json
with open('c:/PWON/CODE rep vonuniverse/webtoonz_minecraft_edu/ess_gapfit/gapfit.json', 'r', encoding='utf-8') as f:
    current_data = json.load(f)

existing = current_data['pozadavky']
print(f'Existing requirements: {len(existing)}')

# Read NPS CSV
nps_requirements = []
with open('c:/PWON/CODE rep vonuniverse/webtoonz_minecraft_edu/ess_gapfit/260123 - ZLK_CSY_GFA_BC_Gap Fit_Final_NPS.csv', 'r', encoding='cp1250') as f:
    reader = csv.reader(f)
    rows = list(reader)
    
    print(f'Total rows in NPS CSV: {len(rows)}')
    
    for i, row in enumerate(rows):
        if len(row) < 5:
            continue
        
        req_id = row[4].strip() if len(row) > 4 else ''
        
        if not req_id or not req_id.startswith('DNPS_'):
            continue
            
        # Extract DNPS number
        try:
            num = int(req_id.split('_')[1])
            if num >= 13 and num <= 76:
                req = {
                    'Oblast': row[1].strip() if len(row) > 1 else '',
                    'Kapitola': row[2].strip() if len(row) > 2 else '',
                    'Název požadavku': row[3].strip() if len(row) > 3 else '',
                    'Požadavek': f'<p>{row[3].strip()}</p>' if len(row) > 3 else '',
                    'ID požadavku': req_id,
                    'Etapa Projektu': row[5].strip() if len(row) > 5 else '',
                    'Typ řešení': row[7].strip() if len(row) > 7 else '',
                    'Popis řešení': f'<p>{row[6].strip()}</p>' if len(row) > 6 else '<p></p>',
                    'Akceptační kritéria': f'<p>{row[9].strip()}</p>' if len(row) > 9 else '<p></p>',
                    'Odhad': str(row[11]).strip() if len(row) > 11 else '',
                    'Poznámka zákazníka': ''
                }
                nps_requirements.append(req)
                print(f'Added {req_id}')
        except Exception as e:
            pass

print(f'NPS requirements (13-76): {len(nps_requirements)}')

# Read Finance CSV
fin_requirements = []
with open('c:/PWON/CODE rep vonuniverse/webtoonz_minecraft_edu/ess_gapfit/260123 - ZLK_CSY_GFA_BC_Gap Fit_Final_Finance.csv', 'r', encoding='cp1250') as f:
    reader = csv.reader(f)
    rows = list(reader)
    
    print(f'Total rows in Finance CSV: {len(rows)}')
    
    for i, row in enumerate(rows):
        if len(row) < 5:
            continue
        
        req_id = row[4].strip() if len(row) > 4 else ''
        
        if not req_id or not req_id.startswith('FIN_'):
            continue
            
        req = {
            'Oblast': row[1].strip() if len(row) > 1 else '',
            'Kapitola': row[2].strip() if len(row) > 2 else '',
            'Název požadavku': row[3].strip() if len(row) > 3 else '',
            'Požadavek': f'<p>{row[3].strip()}</p>' if len(row) > 3 else '',
            'ID požadavku': req_id,
            'Etapa Projektu': row[5].strip() if len(row) > 5 else '',
            'Typ řešení': row[7].strip() if len(row) > 7 else '',
            'Popis řešení': f'<p>{row[6].strip()}</p>' if len(row) > 6 else '<p></p>',
            'Akceptační kritéria': f'<p>{row[9].strip()}</p>' if len(row) > 9 else '<p></p>',
            'Odhad': str(row[11]).strip() if len(row) > 11 else '',
            'Poznámka zákazníka': ''
        }
        fin_requirements.append(req)
        print(f'Added {req_id}')

print(f'Finance requirements (001-100): {len(fin_requirements)}')

# Combine all
all_requirements = existing + nps_requirements + fin_requirements

print(f'Total requirements: {len(all_requirements)}')

# Save to new file
output = {'pozadavky': all_requirements}
with open('c:/PWON/CODE rep vonuniverse/webtoonz_minecraft_edu/ess_gapfit/gapfit.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print('COMPLETE - gapfit.json created successfully')
