import psutil

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Lista de nomes dos processos que você deseja suspender
processos_para_suspender = ["app1.exe", "app2.exe"]

# Função para suspender processos
def suspender_processos(processos):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in processos:
            try:
                p = psutil.Process(proc.info['pid'])
                p.suspend()
                print(f"Processo {proc.info['name']} (PID: {proc.info['pid']}) suspenso.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

# Suspender os processos especificados
suspender_processos(processos_para_suspender)
