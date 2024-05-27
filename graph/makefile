# Compiler and flags
CXX := g++
CXXFLAGS := $(shell cat compile_flags.txt)

# Source files
SRCS = main.cpp \
			 src/adjacency_list.cpp \
			 src/json_defs.cpp \
			 src/fruchterman_reingold.cpp \
			 src/layout.cpp \
			 src/knowledge_graph.cpp

# Object files
OBJS = $(SRCS:.cpp=.o)

# Executable
TARGET = KnowledgeGraph

# Default target
all: $(TARGET)
	@echo "Running the program..."                                            
	./$(TARGET)

# Link object files to create the executable
$(TARGET): $(OBJS)
		$(CXX) $(CXXFLAGS) -o $@ $^

# Compile source files to object files
%.o: %.cpp
		$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up build files
clean:
		rm -f $(OBJS) $(TARGET)

# Phony targets
.PHONY: all clean
