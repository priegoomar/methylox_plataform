<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>METHYLOX™ | Pre-clinical Epigenetic AI Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        .font-serif { font-family: 'Fraunces', serif; }
        .font-sans { font-family: 'Inter', sans-serif; }
        @keyframes scan-line {
            0% { top: 0%; }
            50% { top: 100%; }
            100% { top: 0%; }
        }
        .animate-scan { animation: scan-line 4s linear infinite; }
    </style>
</head>
<body class="font-sans text-[#1e293b] bg-[#f8fafc]">

    <!-- 1. CABECERA INSTITUCIONAL -->
    <header class="w-full py-6 px-12 flex flex-col md:flex-row justify-between items-center bg-white border-b border-[#e2e8f0] sticky top-0 z-50 gap-4">
        <div class="flex items-baseline gap-2">
            <div class="text-2xl font-sans font-black tracking-tight text-[#0f172a]">
                METHYLO<span class="text-[#0891b2]">X</span>™
            </div>
            <div class="text-[10px] font-bold uppercase tracking-wider text-[#64748b] border-l border-gray-300 pl-2 leading-none">
                Plataforma<br>Preclínica
            </div>
        </div>
        <nav class="flex flex-wrap gap-6 md:gap-10 items-center font-medium text-sm text-[#475569]">
            <a href="#protocolo" class="hover:text-[#0891b2] transition">Estrategia</a>
            <a href="#ecosistema" class="hover:text-[#0891b2] transition">Ecosistema</a>
            <a href="#metricas" class="hover:text-[#0891b2] transition">Validación</a>
            <button class="bg-[#0f172a] text-white px-6 py-2.5 rounded-md hover:bg-[#1e293b] transition-all font-semibold text-xs tracking-wider">
                Acceso Técnico
            </button>
        </nav>
    </header>

    <!-- 2. HERO / PRESENTACIÓN DE LA PLATAFORMA -->
    <main id="mision" class="relative w-full bg-[#0f172a] text-white py-24 overflow-hidden">
        <!-- Fondo inmersivo -->
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,#0891b2_0%,transparent_50%)] opacity-20"></div>
        
        <div class="max-w-7xl mx-auto px-12 relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-16 items-center">
            
            <div class="lg:col-span-7 space-y-8">
                <div class="inline-flex items-center gap-2 bg-[#1e293b] px-4 py-1.5 rounded-full border border-[#0891b2]/30">
                    <span class="w-2 h-2 rounded-full bg-[#0891b2] animate-pulse"></span>
                    <span class="text-[10px] font-bold tracking-widest uppercase text-[#bae6fd]">SISTEMA DE ALERTA TEMPRANA ACTIVO</span>
                </div>
                
                <h1 class="text-5xl lg:text-7xl font-serif leading-[0.95] font-bold tracking-tight">
                    <span class="block">Biopsia líquida,</span>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#0891b2] to-[#bae6fd]">precisión oncológica</span>
                </h1>
                
                <p class="text-lg text-[#94a3b8] leading-relaxed max-w-xl">
                    Detección multi-cáncer (MCED) mediante deconvolución epigenética. Identificamos señales tumorales en Stage I, transformando ctDNA en decisiones clínicas accionables.
                </p>

                <div class="flex gap-4">
                    <button onclick="document.getElementById('protocolo').scrollIntoView({behavior: 'smooth'})" class="bg-[#0891b2] hover:bg-[#0ea5e9] text-white px-8 py-4 rounded-xl font-bold transition-all transform hover:scale-105 shadow-[0_0_20px_rgba(8,145,178,0.3)]">
                        Iniciar Diagnóstico In-Silico
                    </button>
                    <button class="bg-transparent border border-[#334155] hover:border-[#0891b2] text-white px-8 py-4 rounded-xl font-bold transition-all">
                        Ver evidencia clínica
                    </button>
                </div>
            </div>
            
            <!-- Elemento visual interactivo (WOW Factor) -->
            <div class="lg:col-span-5 hidden lg:block relative">
                <div class="w-full aspect-square bg-[#1e293b]/50 backdrop-blur-xl border border-[#334155] rounded-3xl p-8 shadow-2xl relative overflow-hidden group">
                    <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                    
                    <!-- Simulación de datos -->
                    <div class="h-full flex flex-col justify-between">
                        <div class="space-y-4">
                            <div class="text-[8px] uppercase tracking-widest text-[#64748b]">Flujo de datos NGS</div>
                            <div class="space-y-2">
                                <div class="h-2 w-full bg-[#0f172a] rounded-full overflow-hidden">
                                    <div class="h-full bg-[#0891b2] animate-[scan-line_2s_linear_infinite]"></div>
                                </div>
                                <div class="h-2 w-3/4 bg-[#0f172a] rounded-full overflow-hidden">
                                    <div class="h-full bg-[#bae6fd] animate-[scan-line_3s_linear_infinite]"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <div class="text-6xl font-bold text-white mb-2">99.8%</div>
                            <div class="text-[#0891b2] text-xs font-bold tracking-widest uppercase">Precisión Epigenética</div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-[#0f172a] p-3 rounded-lg border border-[#0891b2]/20">
                                <div class="text-[#64748b] text-[8px] uppercase">Riesgo</div>
                                <div class="text-white font-bold">Bajo</div>
                            </div>
                            <div class="bg-[#0f172a] p-3 rounded-lg border border-[#0891b2]/20">
                                <div class="text-[#64748b] text-[8px] uppercase">Estado</div>
                                <div class="text-[#10b981] font-bold">Verificado</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- 3. PROTOCOLO TÉCNICO -->
    <section id="protocolo" class="bg-white py-24 border-t border-[#e2e8f0] block w-full">
        <div class="max-w-7xl mx-auto px-12">
            <div class="max-w-3xl mb-16 block">
                <span class="text-[#0891b2] font-bold tracking-[0.2em] uppercase text-xs block mb-2">METODOLOGÍA BIOINFORMÁTICA</span>
                <h2 class="text-4xl font-serif text-[#0f172a] font-bold block">Nuestro Protocolo Técnico</h2>
                <div class="w-12 h-1 bg-[#0891b2] mt-4 rounded-full block"></div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 block w-full">
                <div class="p-10 bg-[#f8fafc] rounded-2xl border border-[#e2e8f0] flex flex-col justify-between min-h-[260px] w-full block">
                    <div class="space-y-4 block">
                        <div class="text-xs font-bold text-[#0891b2] tracking-widest uppercase block">FASE 01 // ENTRADA ÓMICA</div>
                        <h4 class="text-xl font-bold text-[#0f172a] block">Biopsia Líquida</h4>
                        <p class="text-[#64748b] font-light text-sm leading-relaxed block">Aislamiento ultrapreciso de fracciones traza de ctDNA en plasma periférico, optimizado para la captura de señales moleculares tempranas en Etapa I.</p>
                    </div>
                </div>
                <div class="p-10 bg-[#f8fafc] rounded-2xl border border-[#e2e8f0] flex flex-col justify-between min-h-[260px] w-full block">
                    <div class="space-y-4 block">
                        <div class="text-xs font-bold text-[#0891b2] tracking-widest uppercase block">FASE 02 // ESPECIFICIDAD</div>
                        <h4 class="text-xl font-bold text-[#0f172a] block">Detección CRISPR</h4>
                        <p class="text-[#64748b] font-light text-sm leading-relaxed block">Interrogación dirigida mediante un panel cooperativo de 15 sondas in silico diseñado para el reconocimiento de epimutaciones críticas sin PCR previa.</p>
                    </div>
                </div>
                <div class="p-10 bg-[#f8fafc] rounded-2xl border border-[#e2e8f0] flex flex-col justify-between min-h-[260px] w-full block">
                    <div class="space-y-4 block">
                        <div class="text-xs font-bold text-[#0891b2] tracking-widest uppercase block">FASE 03 // DECONVOLUCIÓN</div>
                        <h4 class="text-xl font-bold text-[#0f172a] block">Análisis Epigenético</h4>
                        <p class="text-[#64748b] font-light text-sm leading-relaxed block">Clasificación algorítmica probabilística orientada a la eliminación del ruido biológico subyacente y cálculo instantáneo de la firma de riesgo.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 4. ECOSISTEMA -->
    <section id="ecosistema" class="bg-[#f8fafc] py-16 border-t border-[#e2e8f0] block w-full">
        <div class="max-w-7xl mx-auto px-12">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 block w-full">
                <div class="bg-white p-10 border border-[#e2e8f0] rounded-sm relative group cursor-pointer shadow-[0_4px_20px_rgba(0,0,0,0.01)] hover:shadow-md transition-all flex flex-col justify-between min-h-[180px] w-full block">
                    <div class="block">
                        <div class="w-16 h-[2px] bg-[#bae6fd] mb-6 block"></div>
                        <h3 class="text-2xl font-sans font-bold tracking-tight text-[#0f172a] uppercase text-sm block">CENTRO DE NOTICIAS ÓMICAS</h3>
                    </div>
                    <div class="flex justify-end pt-4 w-full block">
                        <svg class="w-6 h-6 text-[#1e293b] group-hover:text-[#0891b2] group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </div>
                </div>
                <div class="bg-white p-10 border border-[#e2e8f0] rounded-sm relative group cursor-pointer shadow-[0_4px_20px_rgba(0,0,0,0.01)] hover:shadow-md transition-all flex flex-col justify-between min-h-[180px] w-full block">
                    <div class="block">
                        <div class="w-16 h-[2px] bg-[#bae6fd] mb-6 block"></div>
                        <h3 class="text-2xl font-sans font-bold tracking-tight text-[#0f172a] uppercase text-sm block">HISTORIAL DE COHORTES TCGA</h3>
                    </div>
                    <div class="flex justify-end pt-4 w-full block">
                        <svg class="w-6 h-6 text-[#1e293b] group-hover:text-[#0891b2] group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 5. VALIDACIÓN ESTADÍSTICA -->
    <section id="metricas" class="bg-[#f1f5f9] py-24 border-t border-[#e2e8f0] block w-full">
        <div class="max-w-7xl mx-auto px-12">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-center block w-full">
                <div class="lg:col-span-5 space-y-4 block">
                    <span class="text-[#0891b2] font-bold tracking-[0.2em] uppercase text-xs block">RIGOR ESTADÍSTICO</span>
                    <p class="text-base text-[#64748b] font-light leading-relaxed block">Calibración matemática de la firma epigenética entrenada y validada rigurosamente frente a cohortes experimentales masivas de la base de datos global TCGA.</p>
                </div>
                <div class="lg:col-span-7 flex flex-col sm:flex-row gap-6 w-full block">
                    <div class="bg-[#0f172a] text-white p-10 rounded-2xl shadow-md text-center flex-1 space-y-2 block">
                        <div class="text-5xl font-sans font-bold tracking-tight text-[#bae6fd] block">97.2%</div>
                        <h4 class="text-xs font-bold uppercase text-slate-400 tracking-wider block">Sensibilidad Analítica</h4>
                    </div>
                    <div class="bg-white text-[#0f172a] p-10 rounded-2xl shadow-sm text-center flex-1 border border-[#e2e8f0] space-y-2 block">
                        <div class="text-5xl font-sans font-bold tracking-tight text-[#0891b2] block">95.8%</div>
                        <h4 class="text-xs font-bold uppercase text-slate-400 tracking-wider block">Especificidad Analítica</h4>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 6. FOOTER -->
    <footer class="bg-[#0f172a] border-t border-[#1e293b] text-slate-400 py-20 px-12 w-full block">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 text-[11px] font-sans block">
            <div class="space-y-3 block">
                <div class="text-xl font-serif font-bold text-white tracking-wider block">METHYLOX™</div>
                <p class="leading-relaxed text-[#64748b] block">Plataforma bioinformática avanzada para la deconvolución de firmas de metilación aberrantes en ctDNA. Innovación preclínica protegida para detección automatizada en Stage I.</p>
            </div>
            <div class="block">
                <h5 class="text-[#bae6fd] font-bold mb-4 uppercase tracking-widest text-[10px] block">Entorno Técnico</h5>
                <ul class="space-y-2 text-[#94a3b8] block">
                    <li class="block">• Pipeline de Alineación NGS</li>
                    <li class="block">• Panel Multiplex de 15 Sondas</li>
                    <li class="block">• Motores Bayesiano Cooperativos</li>
                </ul>
            </div>
            <div class="block">
                <h5 class="text-[#bae6fd] font-bold mb-4 uppercase tracking-widest text-[10px] block">Documentación</h5>
                <ul class="space-y-2 text-[#94a3b8] block">
                    <li class="block">• Mapeo de Sitios CpG Diana</li>
                    <li class="block">• Línea Base TCGA Multi-Cohorte</li>
                    <li class="block">• Protocolo de De-riesgo IP</li>
                </ul>
            </div>
            <div class="block">
                <h5 class="text-[#ef4444] font-bold mb-4 uppercase tracking-widest text-[10px] block">Acceso Institucional</h5>
                <div class="bg-[#1e293b] border border-[#0891b2] p-4 rounded-lg text-center block">
                    <span class="text-[#bae6fd] font-mono text-[10px] block mb-1">Portal Cifrado Habilitado</span>
                    <span class="text-white font-mono font-bold tracking-wider text-[10px] block">[ ENLACE DE DATOS SECURE ]</span>
                </div>
            </div>
        </div>
        <div class="text-center mt-16 pt-8 border-t border-[#1e293b] text-[#64748b] text-[11px] w-full block">
            © 2026 METHYLOX™ Project. Todos los derechos reservados. Uso académico e institucional bajo Secreto Industrial.
        </div>
    </footer>

</body>
</html>

El mar, 30 jun 2026 a la(s) 2:04 a.m., Lint Brew (brewlint@gmail.com) escribió:
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>METHYLOX™ | Pre-clinical Epigenetic AI Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        .font-serif { font-family: 'Fraunces', serif; }
        .font-sans { font-family: 'Inter', sans-serif; }
        @keyframes scan-line {
            0% { top: 0%; }
            50% { top: 100%; }
            100% { top: 0%; }
        }
        .animate-scan { animation: scan-line 4s linear infinite; }
    </style>
</head>
<body class="font-sans text-[#1e293b] bg-[#f8fafc]">

    <!-- 1. CABECERA INSTITUCIONAL -->
    <header class="w-full py-6 px-12 flex flex-col md:flex-row justify-between items-center bg-white border-b border-[#e2e8f0] sticky top-0 z-50 gap-4">
        <div class="flex items-baseline gap-2">
            <div class="text-2xl font-sans font-black tracking-tight text-[#0f172a]">
                METHYLO<span class="text-[#0891b2]">X</span>™
            </div>
            <div class="text-[10px] font-bold uppercase tracking-wider text-[#64748b] border-l border-gray-300 pl-2 leading-none">
                Plataforma<br>Preclínica
            </div>
        </div>
        <nav class="flex flex-wrap gap-6 md:gap-10 items-center font-medium text-sm text-[#475569]">
            <a href="#protocolo" class="hover:text-[#0891b2] transition">Estrategia</a>
            <a href="#ecosistema" class="hover:text-[#0891b2] transition">Ecosistema</a>
            <a href="#metricas" class="hover:text-[#0891b2] transition">Validación</a>
            <button class="bg-[#0f172a] text-white px-6 py-2.5 rounded-md hover:bg-[#1e293b] transition-all font-semibold text-xs tracking-wider">
                Acceso Técnico
            </button>
        </nav>
    </header>

    <!-- 2. HERO / PRESENTACIÓN DE LA PLATAFORMA -->
    <main id="mision" class="relative w-full bg-[#0f172a] text-white py-24 overflow-hidden">
        <!-- Fondo inmersivo -->
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,#0891b2_0%,transparent_50%)] opacity-20"></div>
        
        <div class="max-w-7xl mx-auto px-12 relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-16 items-center">
            
            <div class="lg:col-span-7 space-y-8">
                <div class="inline-flex items-center gap-2 bg-[#1e293b] px-4 py-1.5 rounded-full border border-[#0891b2]/30">
                    <span class="w-2 h-2 rounded-full bg-[#0891b2] animate-pulse"></span>
                    <span class="text-[10px] font-bold tracking-widest uppercase text-[#bae6fd]">SISTEMA DE ALERTA TEMPRANA ACTIVO</span>
                </div>
                
                <h1 class="text-5xl lg:text-7xl font-serif leading-[0.95] font-bold tracking-tight">
                    <span class="block">Biopsia líquida,</span>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#0891b2] to-[#bae6fd]">precisión oncológica</span>
                </h1>
                
                <p class="text-lg text-[#94a3b8] leading-relaxed max-w-xl">
                    Detección multi-cáncer (MCED) mediante deconvolución epigenética. Identificamos señales tumorales en Stage I, transformando ctDNA en decisiones clínicas accionables.
                </p>

                <div class="flex gap-4">
                    <button onclick="document.getElementById('protocolo').scrollIntoView({behavior: 'smooth'})" class="bg-[#0891b2] hover:bg-[#0ea5e9] text-white px-8 py-4 rounded-xl font-bold transition-all transform hover:scale-105 shadow-[0_0_20px_rgba(8,145,178,0.3)]">
                        Iniciar Diagnóstico In-Silico
                    </button>
                    <button class="bg-transparent border border-[#334155] hover:border-[#0891b2] text-white px-8 py-4 rounded-xl font-bold transition-all">
                        Ver evidencia clínica
                    </button>
                </div>
            </div>
            
            <!-- Elemento visual interactivo (WOW Factor) -->
            <div class="lg:col-span-5 hidden lg:block relative">
                <div class="w-full aspect-square bg-[#1e293b]/50 backdrop-blur-xl border border-[#334155] rounded-3xl p-8 shadow-2xl relative overflow-hidden group">
                    <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                    
                    <!-- Simulación de datos -->
                    <div class="h-full flex flex-col justify-between">
                        <div class="space-y-4">
                            <div class="text-[8px] uppercase tracking-widest text-[#64748b]">Flujo de datos NGS</div>
                            <div class="space-y-2">
                                <div class="h-2 w-full bg-[#0f172a] rounded-full overflow-hidden">
                                    <div class="h-full bg-[#0891b2] animate-[scan-line_2s_linear_infinite]"></div>
                                </div>
                                <div class="h-2 w-3/4 bg-[#0f172a] rounded-full overflow-hidden">
                                    <div class="h-full bg-[#bae6fd] animate-[scan-line_3s_linear_infinite]"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <div class="text-6xl font-bold text-white mb-2">99.8%</div>
                            <div class="text-[#0891b2] text-xs font-bold tracking-widest uppercase">Precisión Epigenética</div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-[#0f172a] p-3 rounded-lg border border-[#0891b2]/20">
                                <div class="text-[#64748b] text-[8px] uppercase">Riesgo</div>
                                <div class="text-white font-bold">Bajo</div>
                            </div>
                            <div class="bg-[#0f172a] p-3 rounded-lg border border-[#0891b2]/20">
                                <div class="text-[#64748b] text-[8px] uppercase">Estado</div>
                                <div class="text-[#10b981] font-bold">Verificado</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- 3. PROTOCOLO TÉCNICO -->
    <section id="protocolo" class="bg-white py-24 border-t border-[#e2e8f0] block w-full">
        <div class="max-w-7xl mx-auto px-12">
            <div class="max-w-3xl mb-16 block">
                <span class="text-[#0891b2] font-bold tracking-[0.2em] uppercase text-xs block mb-2">METODOLOGÍA BIOINFORMÁTICA</span>
                <h2 class="text-4xl font-serif text-[#0f172a] font-bold block">Nuestro Protocolo Técnico</h2>
                <div class="w-12 h-1 bg-[#0891b2] mt-4 rounded-full block"></div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 block w-full">
                <div class="p-10 bg-[#f8fafc] rounded-2xl border border-[#e2e8f0] flex flex-col justify-between min-h-[260px] w-full block">
                    <div class="space-y-4 block">
                        <div class="text-xs font-bold text-[#0891b2] tracking-widest uppercase block">FASE 01 // ENTRADA ÓMICA</div>
                        <h4 class="text-xl font-bold text-[#0f172a] block">Biopsia Líquida</h4>
                        <p class="text-[#64748b] font-light text-sm leading-relaxed block">Aislamiento ultrapreciso de fracciones traza de ctDNA en plasma periférico, optimizado para la captura de señales moleculares tempranas en Etapa I.</p>
                    </div>
                </div>
                <div class="p-10 bg-[#f8fafc] rounded-2xl border border-[#e2e8f0] flex flex-col justify-between min-h-[260px] w-full block">
                    <div class="space-y-4 block">
                        <div class="text-xs font-bold text-[#0891b2] tracking-widest uppercase block">FASE 02 // ESPECIFICIDAD</div>
                        <h4 class="text-xl font-bold text-[#0f172a] block">Detección CRISPR</h4>
                        <p class="text-[#64748b] font-light text-sm leading-relaxed block">Interrogación dirigida mediante un panel cooperativo de 15 sondas in silico diseñado para el reconocimiento de epimutaciones críticas sin PCR previa.</p>
                    </div>
                </div>
                <div class="p-10 bg-[#f8fafc] rounded-2xl border border-[#e2e8f0] flex flex-col justify-between min-h-[260px] w-full block">
                    <div class="space-y-4 block">
                        <div class="text-xs font-bold text-[#0891b2] tracking-widest uppercase block">FASE 03 // DECONVOLUCIÓN</div>
                        <h4 class="text-xl font-bold text-[#0f172a] block">Análisis Epigenético</h4>
                        <p class="text-[#64748b] font-light text-sm leading-relaxed block">Clasificación algorítmica probabilística orientada a la eliminación del ruido biológico subyacente y cálculo instantáneo de la firma de riesgo.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 4. ECOSISTEMA -->
    <section id="ecosistema" class="bg-[#f8fafc] py-16 border-t border-[#e2e8f0] block w-full">
        <div class="max-w-7xl mx-auto px-12">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 block w-full">
                <div class="bg-white p-10 border border-[#e2e8f0] rounded-sm relative group cursor-pointer shadow-[0_4px_20px_rgba(0,0,0,0.01)] hover:shadow-md transition-all flex flex-col justify-between min-h-[180px] w-full block">
                    <div class="block">
                        <div class="w-16 h-[2px] bg-[#bae6fd] mb-6 block"></div>
                        <h3 class="text-2xl font-sans font-bold tracking-tight text-[#0f172a] uppercase text-sm block">CENTRO DE NOTICIAS ÓMICAS</h3>
                    </div>
                    <div class="flex justify-end pt-4 w-full block">
                        <svg class="w-6 h-6 text-[#1e293b] group-hover:text-[#0891b2] group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </div>
                </div>
                <div class="bg-white p-10 border border-[#e2e8f0] rounded-sm relative group cursor-pointer shadow-[0_4px_20px_rgba(0,0,0,0.01)] hover:shadow-md transition-all flex flex-col justify-between min-h-[180px] w-full block">
                    <div class="block">
                        <div class="w-16 h-[2px] bg-[#bae6fd] mb-6 block"></div>
                        <h3 class="text-2xl font-sans font-bold tracking-tight text-[#0f172a] uppercase text-sm block">HISTORIAL DE COHORTES TCGA</h3>
                    </div>
                    <div class="flex justify-end pt-4 w-full block">
                        <svg class="w-6 h-6 text-[#1e293b] group-hover:text-[#0891b2] group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 5. VALIDACIÓN ESTADÍSTICA -->
    <section id="metricas" class="bg-[#f1f5f9] py-24 border-t border-[#e2e8f0] block w-full">
        <div class="max-w-7xl mx-auto px-12">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-center block w-full">
                <div class="lg:col-span-5 space-y-4 block">
                    <span class="text-[#0891b2] font-bold tracking-[0.2em] uppercase text-xs block">RIGOR ESTADÍSTICO</span>
                    <p class="text-base text-[#64748b] font-light leading-relaxed block">Calibración matemática de la firma epigenética entrenada y validada rigurosamente frente a cohortes experimentales masivas de la base de datos global TCGA.</p>
                </div>
                <div class="lg:col-span-7 flex flex-col sm:flex-row gap-6 w-full block">
                    <div class="bg-[#0f172a] text-white p-10 rounded-2xl shadow-md text-center flex-1 space-y-2 block">
                        <div class="text-5xl font-sans font-bold tracking-tight text-[#bae6fd] block">97.2%</div>
                        <h4 class="text-xs font-bold uppercase text-slate-400 tracking-wider block">Sensibilidad Analítica</h4>
                    </div>
                    <div class="bg-white text-[#0f172a] p-10 rounded-2xl shadow-sm text-center flex-1 border border-[#e2e8f0] space-y-2 block">
                        <div class="text-5xl font-sans font-bold tracking-tight text-[#0891b2] block">95.8%</div>
                        <h4 class="text-xs font-bold uppercase text-slate-400 tracking-wider block">Especificidad Analítica</h4>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 6. FOOTER -->
    <footer class="bg-[#0f172a] border-t border-[#1e293b] text-slate-400 py-20 px-12 w-full block">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 text-[11px] font-sans block">
            <div class="space-y-3 block">
                <div class="text-xl font-serif font-bold text-white tracking-wider block">METHYLOX™</div>
                <p class="leading-relaxed text-[#64748b] block">Plataforma bioinformática avanzada para la deconvolución de firmas de metilación aberrantes en ctDNA. Innovación preclínica protegida para detección automatizada en Stage I.</p>
            </div>
            <div class="block">
                <h5 class="text-[#bae6fd] font-bold mb-4 uppercase tracking-widest text-[10px] block">Entorno Técnico</h5>
                <ul class="space-y-2 text-[#94a3b8] block">
                    <li class="block">• Pipeline de Alineación NGS</li>
                    <li class="block">• Panel Multiplex de 15 Sondas</li>
                    <li class="block">• Motores Bayesiano Cooperativos</li>
                </ul>
            </div>
            <div class="block">
                <h5 class="text-[#bae6fd] font-bold mb-4 uppercase tracking-widest text-[10px] block">Documentación</h5>
                <ul class="space-y-2 text-[#94a3b8] block">
                    <li class="block">• Mapeo de Sitios CpG Diana</li>
                    <li class="block">• Línea Base TCGA Multi-Cohorte</li>
                    <li class="block">• Protocolo de De-riesgo IP</li>
                </ul>
            </div>
            <div class="block">
                <h5 class="text-[#ef4444] font-bold mb-4 uppercase tracking-widest text-[10px] block">Acceso Institucional</h5>
                <div class="bg-[#1e293b] border border-[#0891b2] p-4 rounded-lg text-center block">
                    <span class="text-[#bae6fd] font-mono text-[10px] block mb-1">Portal Cifrado Habilitado</span>
                    <span class="text-white font-mono font-bold tracking-wider text-[10px] block">[ ENLACE DE DATOS SECURE ]</span>
                </div>
            </div>
        </div>
        <div class="text-center mt-16 pt-8 border-t border-[#1e293b] text-[#64748b] text-[11px] w-full block">
            © 2026 METHYLOX™ Project. Todos los derechos reservados. Uso académico e institucional bajo Secreto Industrial.
        </div>
    </footer>

</body>
</html>
