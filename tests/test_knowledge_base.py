import json
import tempfile
import unittest
from pathlib import Path

from src.knowledge_base import generar_knowledge_base


class GenerarKnowledgeBaseTests(unittest.TestCase):
    def test_crea_registros_jsonl_con_metadata_y_solapamiento(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            entrada = raiz / "temarios"
            documento = entrada / "medicina" / "tema.txt"
            documento.parent.mkdir(parents=True)
            documento.write_text("uno dos tres cuatro cinco", encoding="utf-8")
            salida = raiz / "salida" / "knowledge_base.jsonl"

            cantidad = generar_knowledge_base(
                entrada,
                salida,
                tamanio_chunk=3,
                solapamiento=1,
            )

            registros = [
                json.loads(linea)
                for linea in salida.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(cantidad, 2)
            self.assertEqual(list(registros[0]), ["id", "metadata", "text"])
            self.assertEqual([registro["text"] for registro in registros], [
                "uno dos tres",
                "tres cuatro cinco",
            ])
            self.assertEqual(registros[0]["id"], "medicina/tema.txt#chunk-0")
            self.assertEqual(
                registros[0]["metadata"],
                {
                    "category": "medicina",
                    "title": "tema",
                    "source": "medicina/tema.txt",
                    "chunk_index": 0,
                },
            )

    def test_rechaza_un_directorio_sin_documentos(self):
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "vacio"
            entrada.mkdir()

            with self.assertRaisesRegex(ValueError, "No se encontraron archivos"):
                generar_knowledge_base(entrada, Path(temporal) / "salida.jsonl")


if __name__ == "__main__":
    unittest.main()
