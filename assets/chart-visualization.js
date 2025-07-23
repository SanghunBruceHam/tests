
// Chart Visualization for Results
class ChartVisualizer {
  constructor() {
    this.colors = {
      egen: '#ff7eb3',
      teto: '#8ac6ff',
      accent: '#ff6b9d'
    };
  }

  createRadarChart(canvasId, data) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    
    // 간단한 레이더 차트 구현
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 50;
    
    // 배경 그리드
    this.drawRadarGrid(ctx, centerX, centerY, radius, data.labels.length);
    
    // 데이터 폴리곤
    this.drawDataPolygon(ctx, centerX, centerY, radius, data.values, data.labels.length);
    
    // 라벨
    this.drawRadarLabels(ctx, centerX, centerY, radius, data.labels);
  }

  drawRadarGrid(ctx, centerX, centerY, radius, sides) {
    ctx.strokeStyle = 'rgba(255,255,255,0.3)';
    ctx.lineWidth = 1;
    
    // 동심원
    for (let i = 1; i <= 5; i++) {
      ctx.beginPath();
      ctx.arc(centerX, centerY, (radius * i) / 5, 0, 2 * Math.PI);
      ctx.stroke();
    }
    
    // 축선
    for (let i = 0; i < sides; i++) {
      const angle = (i * 2 * Math.PI) / sides - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(
        centerX + Math.cos(angle) * radius,
        centerY + Math.sin(angle) * radius
      );
      ctx.stroke();
    }
  }

  drawDataPolygon(ctx, centerX, centerY, radius, values, sides) {
    ctx.fillStyle = 'rgba(255, 126, 179, 0.3)';
    ctx.strokeStyle = this.colors.egen;
    ctx.lineWidth = 2;
    
    ctx.beginPath();
    for (let i = 0; i < sides; i++) {
      const angle = (i * 2 * Math.PI) / sides - Math.PI / 2;
      const value = values[i] / 100; // 0-1 범위로 정규화
      const x = centerX + Math.cos(angle) * radius * value;
      const y = centerY + Math.sin(angle) * radius * value;
      
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }

  drawRadarLabels(ctx, centerX, centerY, radius, labels) {
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    
    labels.forEach((label, i) => {
      const angle = (i * 2 * Math.PI) / labels.length - Math.PI / 2;
      const x = centerX + Math.cos(angle) * (radius + 20);
      const y = centerY + Math.sin(angle) * (radius + 20);
      
      ctx.fillText(label, x, y);
    });
  }

  createBarChart(canvasId, data) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    
    const barWidth = canvas.width / data.length - 20;
    const maxValue = Math.max(...data.map(d => d.value));
    
    data.forEach((item, i) => {
      const barHeight = (item.value / maxValue) * (canvas.height - 40);
      const x = i * (barWidth + 20) + 10;
      const y = canvas.height - barHeight - 20;
      
      // 바 그리기
      ctx.fillStyle = i % 2 === 0 ? this.colors.egen : this.colors.teto;
      ctx.fillRect(x, y, barWidth, barHeight);
      
      // 라벨
      ctx.fillStyle = '#333';
      ctx.font = '10px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(item.label, x + barWidth / 2, canvas.height - 5);
      
      // 값
      ctx.fillText(item.value + '%', x + barWidth / 2, y - 5);
    });
  }
}

window.ChartVisualizer = ChartVisualizer;
