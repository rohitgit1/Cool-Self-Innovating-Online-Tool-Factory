import os
import random

TOOLS = [
    {
        "name": "enterprise-json-architect",
        "html": r"""<!DOCTYPE html>
<html lang="en" class="antialiased text-gray-900 bg-gray-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise JSON Architect</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-typescript.min.js"></script>
    <style>
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.18); }
        .dark-glass { background: rgba(17, 24, 39, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
        .custom-scrollbar::-webkit-scrollbar { width: 8px; height: 8px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #4b5563; border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #6b7280; }
    </style>
</head>
<body class="min-h-screen flex flex-col font-sans selection:bg-indigo-500 selection:text-white" x-data="jsonArchitect()">

    <!-- Navbar -->
    <nav class="glass sticky top-0 z-50 px-6 py-4 border-b border-gray-200 shadow-sm flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold shadow-lg">JA</div>
            <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">Enterprise JSON Architect</h1>
        </div>
        <div class="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full border border-gray-200">
            <span x-text="statusText" :class="statusColor"></span>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow flex flex-col md:flex-row p-6 gap-6 h-[calc(100vh-73px)]">

        <!-- Input Section -->
        <div class="flex-1 flex flex-col bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden relative">
            <div class="px-4 py-3 bg-gray-50 border-b border-gray-100 flex justify-between items-center">
                <h2 class="text-sm font-semibold text-gray-700 uppercase tracking-wider">Raw JSON Payload</h2>
                <button @click="formatInput" class="text-xs bg-white border border-gray-200 hover:bg-gray-50 text-gray-600 font-medium px-3 py-1.5 rounded-md transition-colors shadow-sm">Format</button>
            </div>
            <textarea
                x-model="rawInput"
                @input="processJSON"
                class="flex-1 w-full p-4 focus:outline-none resize-none font-mono text-sm custom-scrollbar text-gray-800"
                placeholder="Paste large JSON arrays or objects here..."></textarea>
        </div>

        <!-- Output Section -->
        <div class="flex-1 flex flex-col dark-glass rounded-2xl shadow-2xl overflow-hidden border border-gray-700">
            <!-- Tabs -->
            <div class="flex border-b border-gray-700 bg-gray-900/50 p-2 gap-2">
                <template x-for="tab in tabs" :key="tab.id">
                    <button
                        @click="activeTab = tab.id; $nextTick(() => Prism.highlightAll())"
                        class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                        :class="activeTab === tab.id ? 'bg-indigo-600 text-white shadow-lg' : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'">
                        <span x-text="tab.name"></span>
                    </button>
                </template>
                <div class="flex-grow"></div>
                <button @click="copyOutput" class="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg border border-gray-600 transition-colors flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                    Copy
                </button>
            </div>

            <!-- Output Content -->
            <div class="flex-1 overflow-auto custom-scrollbar p-4 relative bg-[#1d1f21]">
                <pre class="m-0! p-0! bg-transparent!"><code :class="'language-' + (activeTab === 'ts' ? 'typescript' : 'json')" x-text="outputContent"></code></pre>
            </div>
        </div>
    </main>

    <script>
        document.addEventListener('alpine:init', () => {
            Alpine.data('jsonArchitect', () => ({
                rawInput: '',
                parsedData: null,
                activeTab: 'ts',
                status: 'idle',
                tabs: [
                    { id: 'ts', name: 'TypeScript Interfaces' },
                    { id: 'schema', name: 'JSON Schema' },
                    { id: 'profile', name: 'Data Profile' }
                ],

                get statusText() {
                    if (this.status === 'idle') return 'Ready';
                    if (this.status === 'error') return 'Invalid JSON';
                    if (this.status === 'success') return 'Parsed Successfully';
                    return 'Processing...';
                },
                get statusColor() {
                    if (this.status === 'error') return 'text-red-600 bg-red-100 border-red-200';
                    if (this.status === 'success') return 'text-green-600 bg-green-100 border-green-200';
                    return 'text-gray-500 bg-gray-100 border-gray-200';
                },
                get outputContent() {
                    if (!this.parsedData) return '// Waiting for valid JSON...';

                    try {
                        if (this.activeTab === 'ts') return this.generateTS(this.parsedData, 'Root');
                        if (this.activeTab === 'schema') return JSON.stringify(this.generateSchema(this.parsedData), null, 2);
                        if (this.activeTab === 'profile') return JSON.stringify(this.profileData(this.parsedData), null, 2);
                    } catch (e) {
                        return '// Error generating output: ' + e.message;
                    }
                },

                formatInput() {
                    try {
                        if (!this.rawInput.trim()) return;
                        const obj = JSON.parse(this.rawInput);
                        this.rawInput = JSON.stringify(obj, null, 2);
                        this.processJSON();
                    } catch(e) {
                        this.status = 'error';
                    }
                },

                processJSON() {
                    if (!this.rawInput.trim()) {
                        this.parsedData = null;
                        this.status = 'idle';
                        return;
                    }
                    try {
                        this.parsedData = JSON.parse(this.rawInput);
                        this.status = 'success';
                        setTimeout(() => Prism.highlightAll(), 50);
                    } catch(e) {
                        this.status = 'error';
                    }
                },

                copyOutput() {
                    navigator.clipboard.writeText(this.outputContent);
                    const btn = event.currentTarget;
                    const originalHTML = btn.innerHTML;
                    btn.innerHTML = 'Copied!';
                    setTimeout(() => btn.innerHTML = originalHTML, 2000);
                },

                getType(val) {
                    if (val === null) return 'null';
                    if (Array.isArray(val)) return 'array';
                    return typeof val;
                },

                // Simplified TS Generation
                generateTS(obj, name = 'Root', interfaces = new Map()) {
                    let ts = '';
                    const type = this.getType(obj);

                    if (type === 'array') {
                        if (obj.length > 0) {
                            this.generateTS(obj[0], name + 'Item', interfaces);
                            return Array.from(interfaces.values()).join('\n\n') + `\n\ntype ${name} = ${name}Item[];`;
                        } else {
                            return `type ${name} = any[];`;
                        }
                    } else if (type === 'object') {
                        let props = [];
                        for (const key in obj) {
                            const valType = this.getType(obj[key]);
                            const safeKey = /^[a-zA-Z_$][0-9a-zA-Z_$]*$/.test(key) ? key : `"${key}"`;
                            if (valType === 'object') {
                                const childName = name + key.charAt(0).toUpperCase() + key.slice(1);
                                this.generateTS(obj[key], childName, interfaces);
                                props.push(`  ${safeKey}: ${childName};`);
                            } else if (valType === 'array') {
                                if (obj[key].length > 0) {
                                    const childName = name + key.charAt(0).toUpperCase() + key.slice(1) + 'Item';
                                    this.generateTS(obj[key][0], childName, interfaces);
                                    props.push(`  ${safeKey}: ${childName}[];`);
                                } else {
                                    props.push(`  ${safeKey}: any[];`);
                                }
                            } else {
                                props.push(`  ${safeKey}: ${valType === 'null' ? 'any' : valType};`);
                            }
                        }
                        const iface = `export interface ${name} {\n${props.join('\n')}\n}`;
                        interfaces.set(name, iface);
                    }

                    return Array.from(interfaces.values()).join('\n\n');
                },

                // Simplified JSON Schema
                generateSchema(obj) {
                    const type = this.getType(obj);
                    let schema = { type };

                    if (type === 'object') {
                        schema.properties = {};
                        for (const key in obj) {
                            schema.properties[key] = this.generateSchema(obj[key]);
                        }
                    } else if (type === 'array') {
                        if (obj.length > 0) {
                            schema.items = this.generateSchema(obj[0]);
                        } else {
                            schema.items = {};
                        }
                    }
                    return schema;
                },

                // Profile
                profileData(obj) {
                    let profile = { keys: 0, arrays: 0, objects: 0, primitives: 0 };
                    const traverse = (node) => {
                        const t = this.getType(node);
                        if (t === 'object') { profile.objects++; Object.keys(node).forEach(k => { profile.keys++; traverse(node[k]); }); }
                        else if (t === 'array') { profile.arrays++; node.forEach(n => traverse(n)); }
                        else { profile.primitives++; }
                    };
                    traverse(obj);
                    return profile;
                }
            }));
        });
    </script>
</body>
</html>"""
    },
    {
        "name": "structured-log-parser",
        "html": r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Structured Log Analyzer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: { extend: { colors: { gray: { 900: '#0f1115', 800: '#1a1d24', 700: '#2b303b' } } } }
        }
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gray-900 text-gray-200 font-sans min-h-screen flex flex-col" x-data="logAnalyzer()">

    <header class="border-b border-gray-800 bg-gray-900/50 backdrop-blur-xl sticky top-0 z-10 px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="bg-blue-600/20 p-2 rounded-lg border border-blue-500/30">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
            </div>
            <h1 class="text-2xl font-bold tracking-tight text-white">Log Analyzer Engine <span class="text-xs font-mono bg-blue-600 text-white px-2 py-0.5 rounded-full ml-2">v2.0</span></h1>
        </div>
        <div class="text-sm text-gray-400 font-mono">
            Processed: <span class="text-white font-bold" x-text="parsedCount"></span> / <span x-text="totalLines"></span> lines
        </div>
    </header>

    <main class="flex-grow p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-81px)]">

        <!-- Left Panel: Input & Config -->
        <div class="lg:col-span-1 flex flex-col gap-4">
            <div class="bg-gray-800 rounded-xl p-4 border border-gray-700 shadow-xl flex-grow flex flex-col">
                <label class="text-sm font-semibold text-gray-400 mb-2 uppercase tracking-wide">1. Regex Extractor (Named Groups)</label>
                <input type="text" x-model="regexPattern" @input="debouncedParse" class="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 font-mono text-sm text-green-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" placeholder="e.g. (?<ip>\S+) \S+ \S+ \[(?<date>[^\]]+)\] &quot;(?<method>\S+) (?<path>\S+) .*?&quot; (?<status>\d+)">
                <p class="text-xs text-gray-500 mt-2">Extract variables using JavaScript named capture groups: <code>(?&lt;name&gt;pattern)</code></p>

                <label class="text-sm font-semibold text-gray-400 mt-6 mb-2 uppercase tracking-wide">2. Raw Log Data</label>
                <textarea x-model="rawLogs" @input="debouncedParse" class="flex-grow w-full bg-gray-900 border border-gray-700 rounded-lg p-4 font-mono text-xs text-gray-300 resize-none focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 custom-scrollbar whitespace-pre" placeholder="Paste Apache, Nginx, or unstructured logs here..."></textarea>
            </div>
        </div>

        <!-- Right Panel: Data Table -->
        <div class="lg:col-span-2 bg-gray-800 rounded-xl border border-gray-700 shadow-xl flex flex-col overflow-hidden">
            <div class="p-4 border-b border-gray-700 bg-gray-800/80 flex justify-between items-center">
                <h2 class="text-sm font-semibold text-gray-300 uppercase tracking-wide">Structured Output Table</h2>
                <input type="text" x-model="filterQuery" class="bg-gray-900 border border-gray-700 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:border-blue-500" placeholder="Filter rows...">
            </div>

            <div class="flex-grow overflow-auto custom-scrollbar relative">
                <template x-if="columns.length === 0">
                    <div class="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
                        <svg class="w-12 h-12 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        <p>No named capture groups matched.</p>
                        <p class="text-xs mt-1">Adjust your regex or paste valid logs.</p>
                    </div>
                </template>

                <table class="w-full text-left border-collapse" x-show="columns.length > 0">
                    <thead class="sticky top-0 bg-gray-900 z-10 shadow">
                        <tr>
                            <template x-for="col in columns" :key="col">
                                <th class="px-4 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-gray-700 whitespace-nowrap" x-text="col"></th>
                            </template>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-700/50">
                        <template x-for="(row, idx) in filteredRows" :key="idx">
                            <tr class="hover:bg-gray-700/30 transition-colors">
                                <template x-for="col in columns" :key="col">
                                    <td class="px-4 py-3 text-sm font-mono whitespace-nowrap max-w-[300px] truncate" :title="row[col]">
                                        <!-- Add semantic coloring for status codes etc if possible -->
                                        <span x-text="row[col] || '-'"
                                            :class="col.toLowerCase().includes('status') ?
                                                (String(row[col]).startsWith('2') ? 'text-green-400' :
                                                 String(row[col]).startsWith('3') ? 'text-blue-400' :
                                                 String(row[col]).startsWith('4') ? 'text-yellow-400' :
                                                 String(row[col]).startsWith('5') ? 'text-red-400' : 'text-gray-300')
                                                : 'text-gray-300'"></span>
                                    </td>
                                </template>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <style>
        .custom-scrollbar::-webkit-scrollbar { width: 8px; height: 8px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #374151; border-radius: 4px; border: 2px solid #1f2937; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #4b5563; }
    </style>

    <script>
        document.addEventListener('alpine:init', () => {
            Alpine.data('logAnalyzer', () => ({
                regexPattern: '^(?<ip>\\S+) \\S+ \\S+ \\[(?<date>[^\\]]+)\\] "(?<method>\\S+) (?<path>\\S+) .*?" (?<status>\\d+) (?<size>\\d+)',
                rawLogs: '127.0.0.1 - - [10/Oct/2023:13:55:36 -0700] "GET /api/v1/users HTTP/1.1" 200 2326\n192.168.1.1 - - [10/Oct/2023:13:55:40 -0700] "POST /api/v1/login HTTP/1.1" 401 123\n10.0.0.5 - - [10/Oct/2023:13:56:01 -0700] "GET /health HTTP/1.1" 200 12\n45.22.19.1 - - [10/Oct/2023:13:57:12 -0700] "GET /assets/style.css HTTP/2.0" 304 0\n127.0.0.1 - - [10/Oct/2023:13:58:05 -0700] "GET /api/v1/data HTTP/1.1" 500 4591',
                parsedRows: [],
                columns: [],
                totalLines: 0,
                parsedCount: 0,
                filterQuery: '',
                debounceTimer: null,

                init() {
                    this.parse();
                },

                debouncedParse() {
                    clearTimeout(this.debounceTimer);
                    this.debounceTimer = setTimeout(() => this.parse(), 300);
                },

                parse() {
                    if (!this.regexPattern || !this.rawLogs) {
                        this.parsedRows = [];
                        this.columns = [];
                        this.totalLines = 0;
                        this.parsedCount = 0;
                        return;
                    }

                    const lines = this.rawLogs.split('\n').filter(l => l.trim() !== '');
                    this.totalLines = lines.length;

                    try {
                        const regex = new RegExp(this.regexPattern);
                        let cols = new Set();
                        let rows = [];
                        let count = 0;

                        for (const line of lines) {
                            const match = regex.exec(line);
                            if (match && match.groups) {
                                rows.push(match.groups);
                                Object.keys(match.groups).forEach(k => cols.add(k));
                                count++;
                            }
                        }

                        this.columns = Array.from(cols);
                        this.parsedRows = rows;
                        this.parsedCount = count;
                    } catch (e) {
                        // Invalid regex
                        this.columns = [];
                        this.parsedRows = [];
                        this.parsedCount = 0;
                    }
                },

                get filteredRows() {
                    if (!this.filterQuery) return this.parsedRows;
                    const q = this.filterQuery.toLowerCase();
                    return this.parsedRows.filter(row => {
                        return Object.values(row).some(val => String(val).toLowerCase().includes(q));
                    });
                }
            }));
        });
    </script>
</body>
</html>"""
    },
    {
        "name": "crypto-jwt-studio",
        "html": r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebCrypto JWT Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>
        .bg-pattern { background-image: radial-gradient(#cbd5e1 1px, transparent 1px); background-size: 20px 20px; }
        .token-text { word-break: break-all; font-family: 'JetBrains Mono', monospace; }
        .jwt-header { color: #ec4899; }
        .jwt-payload { color: #8b5cf6; }
        .jwt-signature { color: #0ea5e9; }
    </style>
</head>
<body class="bg-gray-50 text-gray-900 font-sans min-h-screen bg-pattern" x-data="jwtStudio()">

    <div class="max-w-6xl mx-auto p-6 pt-12">

        <div class="text-center mb-10">
            <h1 class="text-4xl font-extrabold tracking-tight text-gray-900 mb-2">WebCrypto <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-purple-500 to-sky-500">JWT Studio</span></h1>
            <p class="text-lg text-gray-600">Secure, client-side JWT generation and decoding using Native WebCrypto API.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

            <!-- Encode Section -->
            <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden flex flex-col">
                <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
                    <h2 class="font-bold text-gray-800 flex items-center gap-2">
                        <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                        Encoder / Signer
                    </h2>
                </div>

                <div class="p-6 flex-grow flex flex-col gap-4">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-1">Header (JSON)</label>
                        <textarea x-model="headerStr" class="w-full h-24 p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500" @input="signToken"></textarea>
                    </div>

                    <div class="flex-grow flex flex-col">
                        <label class="block text-sm font-semibold text-gray-700 mb-1">Payload (JSON)</label>
                        <textarea x-model="payloadStr" class="w-full flex-grow p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500 min-h-[150px]" @input="signToken"></textarea>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-1 flex justify-between">
                            <span>Secret (HMAC SHA-256)</span>
                            <button @click="generateRandomSecret" class="text-xs text-purple-600 hover:text-purple-800 font-medium">Generate Random</button>
                        </label>
                        <input type="text" x-model="secret" class="w-full p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500" @input="signToken">
                    </div>
                </div>
            </div>

            <!-- Decode Section -->
            <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden flex flex-col">
                <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
                    <h2 class="font-bold text-gray-800 flex items-center gap-2">
                        <svg class="w-5 h-5 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                        Encoded Token
                    </h2>
                </div>

                <div class="p-6 flex-grow flex flex-col gap-4">
                    <div class="bg-gray-50 border border-gray-200 rounded-xl p-4 min-h-[150px] relative">
                        <template x-if="tokenError">
                            <div class="absolute inset-0 flex items-center justify-center text-red-500 font-medium bg-gray-50/80 rounded-xl z-10" x-text="tokenError"></div>
                        </template>
                        <div class="token-text text-lg break-all leading-relaxed" style="font-family: monospace;">
                            <span class="jwt-header font-bold" x-text="tokenParts.header"></span><span class="text-gray-400 font-bold" x-show="tokenParts.header">.</span><span class="jwt-payload font-bold" x-text="tokenParts.payload"></span><span class="text-gray-400 font-bold" x-show="tokenParts.payload">.</span><span class="jwt-signature font-bold" x-text="tokenParts.signature"></span>
                        </div>
                    </div>

                    <div class="flex gap-4">
                        <button @click="copyToken" class="flex-1 bg-white border border-gray-300 text-gray-700 font-semibold py-3 px-4 rounded-lg hover:bg-gray-50 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 flex justify-center items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                            Copy Token
                        </button>
                    </div>

                    <div class="mt-4 flex-grow">
                        <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Signature Status</h3>
                        <div class="p-4 rounded-lg border flex items-center gap-3" :class="isSignatureValid ? 'bg-green-50 border-green-200 text-green-700' : 'bg-red-50 border-red-200 text-red-700'">
                            <svg x-show="isSignatureValid" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <svg x-show="!isSignatureValid" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span class="font-medium" x-text="isSignatureValid ? 'Signature Verified' : 'Invalid Signature'"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Utilities for Base64Url
        const b64u = {
            encode: (str) => btoa(unescape(encodeURIComponent(str))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''),
            encodeBytes: (bytes) => btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''),
            decode: (str) => decodeURIComponent(escape(atob((str + '==='.slice((str.length + 3) % 4)).replace(/-/g, '+').replace(/_/g, '/'))))
        };

        document.addEventListener('alpine:init', () => {
            Alpine.data('jwtStudio', () => ({
                headerStr: '{\n  "alg": "HS256",\n  "typ": "JWT"\n}',
                payloadStr: '{\n  "sub": "1234567890",\n  "name": "Enterprise User",\n  "admin": true,\n  "iat": ' + Math.floor(Date.now()/1000) + '\n}',
                secret: 'your-256-bit-secret',
                tokenParts: { header: '', payload: '', signature: '' },
                tokenError: '',
                isSignatureValid: false,

                init() {
                    this.signToken();
                },

                generateRandomSecret() {
                    const array = new Uint8Array(32);
                    window.crypto.getRandomValues(array);
                    this.secret = Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
                    this.signToken();
                },

                async signToken() {
                    this.tokenError = '';
                    try {
                        // Validate JSON
                        JSON.parse(this.headerStr);
                        JSON.parse(this.payloadStr);

                        const encodedHeader = b64u.encode(this.headerStr);
                        const encodedPayload = b64u.encode(this.payloadStr);
                        const dataToSign = `${encodedHeader}.${encodedPayload}`;

                        // WebCrypto HMAC SHA-256
                        const enc = new TextEncoder();
                        const keyMaterial = await window.crypto.subtle.importKey(
                            'raw',
                            enc.encode(this.secret),
                            { name: 'HMAC', hash: 'SHA-256' },
                            false,
                            ['sign']
                        );

                        const signatureBuffer = await window.crypto.subtle.sign(
                            'HMAC',
                            keyMaterial,
                            enc.encode(dataToSign)
                        );

                        const encodedSignature = b64u.encodeBytes(signatureBuffer);

                        this.tokenParts = {
                            header: encodedHeader,
                            payload: encodedPayload,
                            signature: encodedSignature
                        };
                        this.isSignatureValid = true;

                    } catch (e) {
                        this.tokenError = "Invalid JSON input.";
                        this.isSignatureValid = false;
                        this.tokenParts = { header: '', payload: '', signature: '' };
                    }
                },

                copyToken() {
                    const fullToken = `${this.tokenParts.header}.${this.tokenParts.payload}.${this.tokenParts.signature}`;
                    if (fullToken.length > 2) {
                        navigator.clipboard.writeText(fullToken);
                    }
                }
            }));
        });
    </script>
</body>
</html>"""
    }
]

def main():
    current_tool = ""
    try:
        if os.path.exists(".current_tool"):
            with open(".current_tool", "r") as f:
                current_tool = f.read().strip()
    except Exception:
        pass

    available_tools = [t for t in TOOLS if t["name"] != current_tool]
    if not available_tools:
        available_tools = TOOLS

    selected = random.choice(available_tools)

    with open("index.html", "w") as f:
        f.write(selected["html"])

    with open(".current_tool", "w") as f:
        f.write(selected["name"])

    print(f"Deployed tool: {selected['name']}")

if __name__ == "__main__":
    main()
