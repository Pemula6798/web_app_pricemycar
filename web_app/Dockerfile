# Gunakan image Python slim resmi
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Salin requirements.txt terlebih dahulu agar build cache lebih cepat
COPY requirements.txt .

# Install semua dependensi python
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode aplikasi ke dalam container
COPY . .

# Hugging Face Spaces mewajibkan aplikasi mendengarkan pada port 7860
ENV PORT=7860
EXPOSE 7860

# Jalankan Flask menggunakan Gunicorn di port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
