import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const COLORS = ['#D4AF37', '#10b981', '#06b6d4', '#ef4444', '#8b5cf6', '#f59e0b'];

export default function ChartWrapper({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="chart-wrapper glass-card">
      <h3 className="chart-title gradient-text">Data Visualization</h3>
      <div className="chart-container-inner">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(10, 10, 10, 0.85)', 
                borderColor: 'rgba(212, 175, 55, 0.4)',
                borderRadius: '8px',
                color: '#fff'
              }}
              itemStyle={{ color: '#fff' }}
            />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              wrapperStyle={{ fontSize: '12px', color: '#e5e5e5' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
