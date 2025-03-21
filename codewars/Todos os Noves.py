print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def sort_textbooks(textbooks):
  """
  Sorts a list of textbooks by subject in a case-insensitive manner.



  Args:
      textbooks (list): A list of strings representing textbook subjects.

  Returns:
      list: A new list containing the sorted textbooks.
  """

  # Sort the list using a case-insensitive key function
  return sorted(textbooks, key=lambda x: x.upper())

# Example usage
textbooks = ["matemática avançada", "Física para engenheiros", "programação orientada a objetos", "introdução à química", "Matemática Avançada"]
sorted_textbooks = sort_textbooks(textbooks)

print("Livros didáticos classificados por assunto:")
for textbook in sorted_textbooks:
  print(textbook)
