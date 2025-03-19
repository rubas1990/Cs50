#include "helpers.h"
#include <cs50.h>
#include <math.h>
#include <stdint.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float avg = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            int rounded_avg = round(avg);

            image[i][j].rgbtRed = rounded_avg;
            image[i][j].rgbtGreen = rounded_avg;
            image[i][j].rgbtBlue = rounded_avg;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int SepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen +
                                 0.189 * image[i][j].rgbtBlue);
            int SepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen +
                                   0.168 * image[i][j].rgbtBlue);
            int SepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen +
                                  0.131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = SepiaRed > 255 ? 255 : SepiaRed;
            image[i][j].rgbtGreen = SepiaGreen > 255 ? 255 : SepiaGreen;
            image[i][j].rgbtBlue = SepiaBlue > 255 ? 255 : SepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Crear una copia de la imagen original
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Iterar sobre cada píxel de la imagen
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Inicializar los valores de rojo, verde y azul para el píxel actual
            int red = 0;
            int green = 0;
            int blue = 0;

            // Contar el número de píxeles vecinos
            int count = 0;

            // Iterar sobre los píxeles vecinos
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    // Calcular las coordenadas del píxel vecino
                    int x = i + k;
                    int y = j + l;

                    // Verificar si el píxel vecino está dentro de la imagen
                    if (x >= 0 && x < height && y >= 0 && y < width)
                    {
                        // Sumar los valores de rojo, verde y azul del píxel vecino
                        red += copy[x][y].rgbtRed;
                        green += copy[x][y].rgbtGreen;
                        blue += copy[x][y].rgbtBlue;

                        // Incrementar el contador de píxeles vecinos
                        count++;
                    }
                }
            }

            // Calcular el promedio de los valores de rojo, verde y azul
            int avgRed = round((float) red / count);
            int avgGreen = round((float) green / count);
            int avgBlue = round((float) blue / count);

            // Asignar los valores promedio a cada componente de color
            image[i][j].rgbtRed = avgRed > 255 ? 255 : avgRed;
            image[i][j].rgbtGreen = avgGreen > 255 ? 255 : avgGreen;
            image[i][j].rgbtBlue = avgBlue > 255 ? 255 : avgBlue;
        }
    }
}
