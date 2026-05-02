let lastSavedFilename = ""; 

const canvas = new fabric.Canvas('canvas', { backgroundColor: '#fff' });
const COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFA500", "#800080"];
let isDrawing = false, rect, origX, origY;

function updateYOLODisplay() {
    const display = document.getElementById('yoloList');
    if (!display) return;
    const objects = canvas.getObjects('rect');
    const yoloLines = objects.map(obj => {
        const id = obj.data?.class_id || document.getElementById('classId').value;
        const w = obj.getScaledWidth();
        const h = obj.getScaledHeight();
        const x_center = (obj.left + w / 2) / 640;
        const y_center = (obj.top + h / 2) / 640;
        const norm_w = w / 640;
        const norm_h = h / 640;
        return `${id} ${x_center.toFixed(6)} ${y_center.toFixed(6)} ${norm_w.toFixed(6)} ${norm_h.toFixed(6)}`;
    });
    display.innerHTML = yoloLines.length ? yoloLines.join('<br>') : "Nenhuma box.";
}

// 1. Carregar Imagem
document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(f) {
        const imgElement = new Image();
        imgElement.src = f.target.result;
        imgElement.onload = function() {
            const fabricImage = new fabric.Image(imgElement);
            canvas.clear();
            fabricImage.set({
                scaleX: 640 / imgElement.width,
                scaleY: 640 / imgElement.height,
                selectable: false,
                evented: false
            });
            canvas.setBackgroundImage(fabricImage, canvas.renderAll.bind(canvas));
        };
    };
    reader.readAsDataURL(file);
});

// 2. Lógica de Desenho
canvas.on('mouse:down', function(o) {
    if (document.getElementById('mode').value !== 'draw') return;
    isDrawing = true;
    const pointer = canvas.getPointer(o.e);
    origX = pointer.x; origY = pointer.y;
    rect = new fabric.Rect({
        left: origX, top: origY, width: 0, height: 0,
        fill: 'transparent', stroke: COLORS[document.getElementById('classId').value % COLORS.length],
        strokeWidth: 3, selectable: false,
        data: { class_id: document.getElementById('classId').value }
    });
    canvas.add(rect);
});

canvas.on('mouse:move', function(o) {
    if (!isDrawing) return;
    const pointer = canvas.getPointer(o.e);
    if (origX > pointer.x) rect.set({ left: pointer.x });
    if (origY > pointer.y) rect.set({ top: pointer.y });
    rect.set({ width: Math.abs(origX - pointer.x), height: Math.abs(origY - pointer.y) });
    canvas.renderAll();
    updateYOLODisplay();
});

canvas.on('mouse:up', () => { isDrawing = false; rect?.setCoords(); });
canvas.on('object:moving', updateYOLODisplay);
canvas.on('object:scaling', updateYOLODisplay);

document.getElementById('mode').addEventListener('change', function() {
    const isSelect = this.value === 'select';
    canvas.getObjects().forEach(obj => obj.selectable = isSelect);
    canvas.discardActiveObject().renderAll();
});

// --- FUNÇÕES DE API ---

// ESSA FUNÇÃO ESTAVA FALTANDO NO SEU CÓDIGO ANTERIOR
async function saveAnnotations() {
    if (!canvas.backgroundImage) return alert("Carregue uma imagem!");
    
    const objects = canvas.getObjects('rect');
    if (objects.length === 0) return alert("Desenhe pelo menos uma box!");

    // 1. Pega o ID da classe e gera o nome EXATO que o servidor espera
    const classId = document.getElementById('classId').value;
    const timestamp = Date.now();
    const filename = `${classId}_img_${timestamp}`; 

    // 2. Prepara a imagem (Corrigido o split)
    const dataURL = canvas.toDataURL({ format: 'jpeg', quality: 0.8 });
    const base64Image = dataURL.split(',')[1]; // Pegamos apenas a parte dos dados

    // 3. Mapeia os labels
    const yoloLabels = objects.map(obj => {
        const id = obj.data?.class_id || classId;
        const w = obj.getScaledWidth();
        const h = obj.getScaledHeight();
        const x_center = (obj.left + w / 2) / 640;
        const y_center = (obj.top + h / 2) / 640;
        const norm_w = w / 640;
        const norm_h = h / 640;
        return `${id} ${x_center.toFixed(6)} ${y_center.toFixed(6)} ${norm_w.toFixed(6)} ${norm_h.toFixed(6)}`;
    });

    try {
        const response = await fetch('/save_yolo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                image_b64: base64Image, 
                filename: filename, 
                labels: yoloLabels 
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // 4. Guarda o nome com .jpg para a rota de Build encontrar
            lastSavedFilename = filename + ".jpg"; 
            alert("Sucesso! Imagem salva como: " + lastSavedFilename);
        } else {
            alert("Erro no servidor: " + result.msg);
        }
    } catch (e) { 
        console.error(e);
        alert("Erro na requisição de salvamento."); 
    }
}


async function runAction(route) {
    const btnTrain = document.getElementById('btnTrain');
    const originalText = btnTrain.innerHTML;

    try {
        const fileInput = document.getElementById("imageInput");
        const file = fileInput.files[0];

        if (!file) {
            return alert("⚠️ Selecione uma imagem primeiro!");
        }

        const formData = new FormData();
        formData.append("image", file);

        btnTrain.disabled = true;
        btnTrain.innerHTML = "⏳ Treinando...";

        const response = await fetch(route, {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        alert(result.status || result.msg || "Operação concluída");

    } catch (e) {
        alert("Erro: " + e.message);
    } finally {
        btnTrain.disabled = false;
        btnTrain.innerHTML = originalText;
    }
}

async function predictFromVal() {
    try {
        const response = await fetch('/predict', { method: 'POST' });
        const result = await response.json();
        const imgElement = new Image();
        imgElement.src = "data:image/jpeg;base64," + result.image_b64;
        imgElement.onload = function() {
            const fabricImage = new fabric.Image(imgElement);
            canvas.clear();
            fabricImage.set({ scaleX: 640/imgElement.width, scaleY: 640/imgElement.height, selectable: false });
            canvas.setBackgroundImage(fabricImage, canvas.renderAll.bind(canvas));
            result.detections.forEach(det => {
                canvas.add(new fabric.Rect({
                    left: det.x1, top: det.y1, width: det.x2-det.x1, height: det.y2-det.y1,
                    fill: 'transparent', stroke: '#00FF00', strokeWidth: 2
                }));
            });
        };
    } catch (e) { alert("Erro no predict"); }
}

// Atalhos e Limpeza
window.addEventListener('keydown', (e) => {
    if (e.key === "Delete" || e.key === "Backspace") {
        canvas.getActiveObjects().forEach(obj => canvas.remove(obj));
        canvas.discardActiveObject().renderAll();
        updateYOLODisplay();
    }
});

// Eventos de Botões
document.getElementById('btnSave').addEventListener('click', saveAnnotations);
document.getElementById('btnBuild').addEventListener('click', () => runAction('/build_dataset'));
document.getElementById('btnTrain').addEventListener('click', () => runAction('/train'));
document.getElementById('btnPredict').addEventListener('click', () => runAction('/predict'));
document.getElementById('btnClear').addEventListener('click', () => {
    if (confirm("Limpar tudo?")) {
        canvas.getObjects('rect').forEach(obj => canvas.remove(obj));
        updateYOLODisplay();
    }
});
